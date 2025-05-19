import pytest
from ssg.game.board import GameBoard
from ssg.utils import Point


@pytest.fixture
def empty_board():
    return GameBoard([])


some_turns = [
    Point(0, 0),
    Point(1, 0),
    Point(0, 1),
    Point(1, 1),
    Point(0, 2),
    Point(1, 2),
    Point(0, 3),
]


@pytest.fixture
def populated_board():
    return GameBoard(some_turns)


def test_empty_board_initialization(empty_board: GameBoard):
    for row in empty_board:
        assert all(cell == -1 for cell in row)


def test_board_turns_tracking(populated_board: GameBoard):
    assert populated_board.turns == some_turns


def test_board_turn_values_correctness(populated_board: GameBoard):
    expected = {p: t for t, p in enumerate(some_turns)}

    for p, t in expected.items():
        assert populated_board[p[1]][p[0]] == t


def test_is_free_on_empty_board(empty_board: GameBoard):
    assert empty_board.is_free(3, 3) is True
    assert empty_board.is_free(0, 0) is True
    assert empty_board.is_free(-1, 0) is False
    assert empty_board.is_free(0, 7) is False


def test_is_free_on_populated_board(populated_board: GameBoard):
    assert populated_board.is_free(0, 0) is False
    assert populated_board.is_free(1, 2) is False
    assert populated_board.is_free(2, 2) is True


def test_duplicate_turn():
    turns = [*some_turns, some_turns[0]]

    pytest.raises(ValueError, lambda: GameBoard(turns))
