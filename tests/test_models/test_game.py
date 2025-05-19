from sqlite3 import Connection
import pytest

from ssg.models.player import Player
from ssg.models.game import Game
from ssg.game import GameStatus


@pytest.fixture
def player_ids(db: Connection) -> tuple[int, int]:
    p0 = Player.get_or_create(db, "foo")
    p1 = Player.get_or_create(db, "bar")
    return (p0.id, p1.id)


@pytest.fixture
def game(db: Connection, player_ids: tuple[int, int]) -> Game:
    return Game.create(db, code="TEST1", player_0=player_ids[0], player_1=player_ids[1])


def test_create_and_load_game(db: Connection, game: Game):
    loaded = Game.load(db, "TEST1")
    assert loaded is not None
    assert loaded.id == game.id
    assert loaded.player_0 == game.player_0
    assert loaded.player_1 == game.player_1
    assert loaded.code == game.code


def test_game_str_does_not_crash(game: Game):
    assert isinstance(str(game), str)
    assert "TEST1" in str(game)


def test_join_fills_missing_player_slot(db: Connection, player_ids: tuple[int, int]):
    g = Game.create(db, code="JOINTEST")
    assert g.player_0 is None and g.player_1 is None

    ok = g.join(player_ids[0])
    assert ok
    assert g.player_0 == player_ids[0]

    ok = g.join(player_ids[1])
    assert ok
    assert g.player_1 == player_ids[1]

    ok = g.join(player_ids[0])
    assert not ok  # already full


def test_has_all_players_flag(game: Game):
    assert game.has_all_players is True


def test_game_play_and_turns(game: Game):
    assert game.next_turn == 0
    game.play(0, 0)
    assert game.next_turn == 1
    game.play(0, 1)
    assert game.next_turn == 2
    assert game.status == GameStatus.UNDECIDED


def test_legal_move_detection(game: Game):
    legal = game.state.legal_cells
    assert any(game.is_legal_move(p[0], p[1]) for p in legal)
    assert not game.is_legal_move(-1, -1)


def test_game_status_win(db: Connection, player_ids: tuple[int, int]):
    g = Game.create(db, player_0=player_ids[0], player_1=player_ids[1])

    # vertical win for player 0 (assumes player 0 always goes first)
    g.play(0, 0)  # p0
    g.play(1, 0)  # p1
    g.play(0, 1)  # p0
    g.play(1, 1)  # p1
    g.play(0, 2)  # p0
    g.play(1, 2)  # p1
    g.play(0, 3)  # p0

    assert g.status == GameStatus.WIN
    assert g.winner == player_ids[0]


def test_game_status_undecided(db: Connection, player_ids: tuple[int, int]):
    g = Game.create(db, player_0=player_ids[0], player_1=player_ids[1])

    g.play(0, 0)  # p0
    g.play(1, 0)  # p1
    g.play(6, 0)  # p0
    g.play(6, 1)  # p1
    g.play(0, 2)  # p0
    g.play(1, 2)  # p1
    g.play(0, 3)  # p0

    assert g.status == GameStatus.UNDECIDED
