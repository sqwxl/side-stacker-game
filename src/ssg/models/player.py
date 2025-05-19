from sqlite3 import Connection
from typing import Self, override


class Player:
    db: Connection
    _id: int
    token: str

    def __init__(self, db: Connection, id: int, token: str):
        self.db = db
        self._id = id
        self.token = token

    @override
    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Player)
            and self._id == other._id
            and self.token == other.token
        )

    @property
    def id(self):
        return self._id

    @classmethod
    def load(cls, db: Connection, token: str) -> Self | None:
        row = db.execute("select id from player where token = ?", (token,)).fetchone()

        if not row:
            return None

        return cls(db, row["id"], token)

    @classmethod
    def create(cls, db: Connection, token: str) -> Self:
        if not token:
            raise ValueError("Player token cannot be empty")

        id = db.execute(
            """
            insert into player (token) values (?) on conflict (token) do update set token = excluded.token returning id
            """,
            (token,),
        ).fetchone()["id"]

        db.commit()

        return cls(db, id, token)

    @classmethod
    def get_or_create(cls, db: Connection, token: str) -> Self:
        return cls.load(db, token) or cls.create(db, token)
