from dataclasses import dataclass
from sqlite3 import Connection
from typing import Self


@dataclass
class Move:
    db: Connection
    _id: int
    game_id: int
    turn: int
    col: int
    row: int

    def __init__(
        self, db: Connection, id: int, game_id: int, turn: int, col: int, row: int
    ) -> None:
        self.db = db
        self._id = id
        self.game_id = game_id
        self.turn = turn
        self.col = col
        self.row = row

    def __iter__(self):
        return iter((self.col, self.row, self.turn))

    @property
    def id(self):
        return self._id

    @classmethod
    def create(
        cls, db: Connection, game_id: int, turn: int, col: int, row: int
    ) -> Self:
        id = db.execute(
            """
            insert into move (game_id, turn, col, row)
            values (?, ?, ?, ?) on conflict (game_id, col, row)
            do update set id = excluded.id
            returning id
            """,
            (game_id, turn, col, row),
        ).fetchone()["id"]

        db.commit()

        return cls(db, id, game_id, turn, col, row)

    @classmethod
    def for_game(cls, db: Connection, game_id: int) -> list[Self]:
        row = db.execute(
            "select id, game_id, turn, col, row from move where game_id = ? order by turn",
            (game_id,),
        ).fetchall()

        return [
            cls(db, r["id"], r["game_id"], r["turn"], r["col"], r["row"]) for r in row
        ]
