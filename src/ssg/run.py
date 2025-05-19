import asyncio
import json
from pathlib import Path
from typing import cast
from uuid import uuid4

from quart import (
    Quart,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    websocket,
)
from werkzeug.datastructures import MultiDict

from ssg.ai import AIPlayerMap, AIPlayerID
from ssg.db import connect_db
from ssg.forms import GameForm
from ssg.game import GameStatus
from ssg.models import Game, Player
from ssg.ws.actions import PlayAction, parse_action
from ssg.ws.broker import Broker, BrokerHub

app = Quart(__name__, static_folder="./static", static_url_path="/static")

app.config["DATABASE"] = Path(app.root_path) / "ssg.db"
app.secret_key = "not_so_secret_secret"


def init_db(app: Quart):
    db = connect_db(app)
    with open(Path(app.root_path) / "schema.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()

    return db


def run() -> None:
    app.run()


@app.before_request
async def clear_jinja_cache():
    app.jinja_env.cache = {}


@app.before_request
async def get_db():
    if not hasattr(g, "db"):
        g.db = connect_db(app)


@app.before_request
async def set_session():
    session.permanent = True
    if session.get("token") is None:
        session["token"] = str(uuid4())


@app.route("/", methods=["GET", "POST"])
async def index():
    if request.method == "GET":
        return await render_template("index.html")

    form = cast(MultiDict[str, str], await request.form)

    token = session.get("token")
    assert token

    player = Player.get_or_create(g.db, token)

    game = GameForm(player.id, form).save(g.db)

    return redirect(url_for("game", code=game.code))


@app.get("/<string:code>")
async def game(code: str):
    game = Game.load(g.db, code)

    if game is None:
        await flash(f"Failed to find game with code {code}")
        return redirect(url_for("index"))

    if game.status != GameStatus.UNDECIDED:
        return await render_template("record.html", game=game)

    token = session.get("token")
    assert token

    player = Player.get_or_create(g.db, token)

    if player.id not in [game.player_0, game.player_1]:
        if not game.has_all_players:
            success = game.join(player.id)
            if not success:
                await flash("Failed to join the game.")

    return await render_template("game.html", game=game, player=player)


brokers = BrokerHub()


async def _receive(broker: Broker) -> None:
    while True:
        message: str = await websocket.receive()

        app.logger.debug(f"WS: raw ws message: {message}")

        await broker.publish(message)


async def _ws_flash(message: str):
    await websocket.send(await render_template("flash.html", message=message))


async def _ws_send_board(game: Game, player: Player):
    await websocket.send(await render_template("board.html", game=game, player=player))


@app.websocket("/<string:code>/ws")
async def ws(code: str) -> None:
    await get_db()

    game = Game.load(g.db, code)
    if not game:
        await _ws_flash("Server error. Try refreshing?")
        raise Exception(f"Game with code {code} not found. This is a bug!")

    token = session.get("token")
    if not token:
        await _ws_flash("Server error. Try refreshing?")
        raise Exception("Missing session token. This is a bug!")

    player = Player.load(g.db, token)
    if not player:
        await _ws_flash("Server error. Try refreshing?")
        raise Exception("Missing player. This is a bug!")

    app.logger.debug(f"Player {player.id} connected to websocket")

    broker = brokers.get(code)

    task = None

    # AI first move
    if game.next_player in AIPlayerID:
        app.add_background_task(_handle_ai_turn, game, broker)

    try:
        task = asyncio.ensure_future(_receive(broker))

        async for raw_message in broker.subscribe(player.id):
            game = Game.load(g.db, code)
            assert game

            if raw_message == SEND_BOARD:
                await _ws_send_board(game, player)

            if game.next_player in AIPlayerID:
                app.add_background_task(_handle_ai_turn, game, broker)

            obj = {}
            try:
                obj = json.loads(raw_message)
            except json.JSONDecodeError:
                pass

            if "action" in obj:
                action = parse_action(obj["action"])
                app.logger.debug(f"WS: Parsed action {action}")

                if isinstance(action, PlayAction):
                    if game.next_player != player.id:
                        app.logger.warning(
                            f"WS: Player {player.id} is trying to play out of turn"
                        )
                        continue

                    col, row = action.payload

                    if not game.is_legal_move(col, row):
                        app.logger.error(
                            f"WS: Got illegal move from player {player.id}: {col},{row}"
                        )
                        continue

                    # Player move
                    game = await _handle_human_turn(game, broker, col, row)

    except asyncio.CancelledError as e:
        broker.connections.pop(player.id)
        raise e
    except Exception as e:
        app.logger.error(e)
        raise e
    finally:
        if task:
            task.cancel()
            await task


SEND_BOARD = "send_board"


async def _broadcast_game(game: Game, broker: Broker) -> None:
    app.logger.debug(f"Publishing game board:\n{game}")

    await broker.publish(SEND_BOARD)


async def _handle_human_turn(game: Game, broker: Broker, col: int, row: int) -> Game:
    game = game.play(col, row)

    await _broadcast_game(game, broker)

    return game


async def _handle_ai_turn(game: Game, broker: Broker):
    ai_player_id = AIPlayerID(game.next_player)

    app.logger.debug("AI player is thinking")

    await asyncio.sleep(0.5)  # Thinking hard :)

    col, row = AIPlayerMap[ai_player_id].play(game.state)

    app.logger.debug(f"AI player {ai_player_id} is making move {col}, {row}")

    game = game.play(col, row)

    await _broadcast_game(game, broker)

    return game


if __name__ == "__main__":
    app.run()
