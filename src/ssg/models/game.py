from secrets import choice
from sqlite3 import Connection
from string import ascii_uppercase
from typing import Any, Self, override


from ssg.game import GameBoard, GameState, GameStatus
from ssg.models.move import Move
from ssg.utils import Point


class Game:
    db: Connection
    _id: int
    code: str
    player_0: int | None
    player_1: int | None
    state: GameState

    def __init__(
        self,
        db: Connection,
        id: int,
        code: str,
        player_0: int | None = None,
        player_1: int | None = None,
    ) -> None:
        self.db = db
        self._id = id
        self.code = code
        self.player_0 = player_0
        self.player_1 = player_1

        turns = [Point(c, r) for c, r, _ in Move.for_game(self.db, self._id)]

        self.state = GameState(turns)

    @override
    def __str__(self) -> str:
        return f"""
            code: {self.code}
            player_0: {self.player_0}
            player_1: {self.player_1}
            turn: {self.next_turn}
            next_player: {self.next_player}
            status: {self.status}
            """

    @property
    def id(self) -> int:
        return self._id

    @property
    def has_all_players(self) -> bool:
        return self.player_0 is not None and self.player_1 is not None

    @property
    def status(self) -> GameStatus:
        return self.state.status

    @property
    def finished(self) -> bool:
        return self.status != GameStatus.UNDECIDED

    @property
    def board(self) -> GameBoard:
        return self.state.board

    @property
    def next_turn(self) -> int | None:
        if self.finished:
            return None

        return self.state.next_turn

    @property
    def next_parity(self) -> int | None:
        if self.finished:
            return None

        return self.state.next_parity

    @property
    def next_player(self) -> int | None:
        if self.finished:
            return None

        return self.player_0 if self.next_parity == 0 else self.player_1

    @property
    def winner(self) -> int | None:
        if not self.finished:
            return None

        return self.player_0 if self.state.winner_parity == 0 else self.player_1

    @property
    def status_message(self) -> str | None:
        if not self.finished:
            color = "🔴" if self.next_parity == 0 else "🔵"
            return f"{color} to play"
        if self.status == GameStatus.DRAW:
            return "It's a draw!"
        if self.status == GameStatus.WIN:
            color = "🔴" if self.state.winner_parity == 0 else "🔵"
            return f"{color} won!"

    def is_legal_move(self, col: int, row: int) -> bool:
        if self.finished:
            return False

        return any(col == c and row == r for c, r in self.state.legal_cells)

    def play(self, col: int, row: int) -> Self:
        if self.finished:
            raise Exception("Tried to play in a finished game")

        Move.create(
            db=self.db, game_id=self.id, turn=self.state.next_turn, col=col, row=row
        )

        turns = [Point(c, r) for c, r, _ in Move.for_game(self.db, self.id)]

        self.state = GameState(turns)

        return self

    def join(self, player_id: int) -> bool:
        if self.player_0 is None:
            self.player_0 = player_id
        elif self.player_1 is None:
            self.player_1 = player_id
        else:
            return False

        self.db.execute(
            "update game set player_0_id = ?, player_1_id = ? where id = ?",
            (self.player_0, self.player_1, self.id),
        )

        self.db.commit()

        return True

    @classmethod
    def load(cls, db: Connection, code: str) -> Self | None:
        row = db.execute(
            "select g.id, g.player_0_id, g.player_1_id from game g where g.code = ?",
            (code,),
        ).fetchone()

        if not row:
            return None

        return cls(db, row["id"], code, row["player_0_id"], row["player_1_id"])

    @classmethod
    def create(
        cls,
        db: Connection,
        code: str | None = None,
        player_0: int | None = None,
        player_1: int | None = None,
    ) -> Self:
        code = code or Game._gen_code()

        row = db.execute(
            """
            insert into game (code, player_0_id, player_1_id)
            values (:code, :player_0, :player_1)
            on conflict(code) do update set
                player_0_id = :player_0,
                player_1_id = :player_1
            returning id
            """,
            {"code": code, "player_0": player_0, "player_1": player_1},
        ).fetchone()

        db.commit()

        return cls(db, row["id"], code, player_0, player_1)

    @staticmethod
    def _gen_code() -> str:
        return "".join(choice(ascii_uppercase) for _ in range(5))

    @classmethod
    def games_for_player(cls, db: Connection, player_id: int) -> list[Self]:
        rows = db.execute(
            "select * from game where player_0_id = ? or player_1_id = ? order by created_on desc",
            (player_id, player_id),
        ).fetchall()

        return list(map(lambda r: cls.from_row(db, r), rows))

    @classmethod
    def from_row(cls, db: Connection, row: Any) -> Self:
        return cls(
            db,
            id=row["id"],
            code=row["code"],
            player_0=row["player_0_id"],
            player_1=row["player_1_id"],
        )
