from sqlite3 import Connection
import pytest
from ssg.models.move import Move


@pytest.fixture
def game_id(db: Connection):
    row = db.execute(
        """
        insert into game (code, player_0_id, player_1_id)
        values (?, 1, 2)
        returning id
        """,
        ("TEST1",),
    ).fetchone()

    db.commit()
    return row["id"]


def test_create_move(db: Connection, game_id: int):
    move = Move.create(db, game_id=game_id, turn=0, col=2, row=3)

    assert isinstance(move, Move)
    assert move.id is not None
    assert move.game_id == game_id
    assert move.turn == 0
    assert move.col == 2
    assert move.row == 3


def test_iter_move_returns_expected_tuple(db: Connection, game_id: int):
    move = Move.create(db, game_id=game_id, turn=1, col=4, row=5)
    assert tuple(move) == (4, 5, 1)


def test_for_game_returns_all_moves_ordered_by_turn(db: Connection, game_id: int):
    Move.create(db, game_id=game_id, turn=2, col=0, row=1)
    Move.create(db, game_id=game_id, turn=1, col=2, row=2)
    Move.create(db, game_id=game_id, turn=3, col=3, row=3)

    moves = Move.for_game(db, game_id=game_id)
    assert [m.turn for m in moves] == [1, 2, 3]

    assert Move.for_game(db, game_id=999) == []

