from ssg.game.engine import GameEngine, GameStatus
from ssg.utils import Point


def test_initial_status_is_undecided():
    turns = [
        Point(0, 0),
        Point(1, 0),
        Point(0, 1),
        Point(1, 1),
        Point(0, 2),
        Point(1, 2),
    ]  # Only 6 moves
    engine = GameEngine(turns)
    assert engine.status == GameStatus.UNDECIDED


def test_vertical_win():
    turns = [
        Point(0, 0),
        Point(1, 0),
        Point(0, 1),
        Point(1, 1),
        Point(0, 2),
        Point(1, 2),
        Point(0, 3),  # 4 in column 0 (vertical win)
    ]
    engine = GameEngine(turns)
    assert engine.status == GameStatus.WIN


def test_horizontal_win():
    turns = [
        Point(0, 0),
        Point(0, 1),
        Point(1, 0),
        Point(1, 1),
        Point(2, 0),
        Point(2, 1),
        Point(3, 0),  # horizontal win on row 0
    ]
    engine = GameEngine(turns)
    assert engine.status == GameStatus.WIN


def test_diagonal_win_nw_se():
    turns = [
        Point(0, 0),
        Point(0, 1),
        Point(1, 1),
        Point(0, 2),
        Point(1, 2),
        Point(0, 3),
        Point(2, 2),
        Point(1, 3),
        Point(2, 3),
        Point(6, 0),
        Point(3, 3),  # Final move for diagonal NW to SE
    ]
    engine = GameEngine(turns)
    assert engine.status == GameStatus.WIN


def test_diagonal_win_ne_sw():
    turns = [
        Point(3, 0),
        Point(2, 0),
        Point(2, 1),
        Point(1, 0),
        Point(1, 1),
        Point(0, 0),
        Point(1, 2),
        Point(0, 1),
        Point(0, 2),
        Point(4, 0),
        Point(0, 3),  # Final move for diagonal NE to SW
    ]
    engine = GameEngine(turns)
    assert engine.status == GameStatus.WIN


def test_draw(no_fours_pattern: list[Point]):
    engine = GameEngine(no_fours_pattern)
    assert engine.status == GameStatus.DRAW


def test_legal_cells():
    turns = [Point(0, 3), Point(6, 3), Point(1, 3), Point(5, 3)]
    engine = GameEngine(turns)
    cells = engine.legal_cells
    assert all(isinstance(p, Point) for p in cells)
    assert any(p == Point(0, 0) for p in cells)
    assert any(p == Point(6, 6) for p in cells)
    assert any(p == Point(2, 3) for p in cells)
    assert any(p == Point(4, 3) for p in cells)
