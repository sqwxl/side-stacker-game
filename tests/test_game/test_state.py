from ssg.game.state import GameState
from ssg.game.engine import GameStatus
from ssg.utils import Point


def test_next_turn_and_next_player():
    # 0 turns → next_turn == 0, next_parity == 0
    state = GameState([])
    assert state.next_turn == 0
    assert state.next_parity == 0

    # 3 turns → next_turn == 3, next_parity == 1
    turns = [Point(0, 0), Point(1, 0), Point(0, 1)]
    state = GameState(turns)
    assert state.next_turn == 3
    assert state.next_parity == 1


def test_status_delegates_to_engine():
    turns = [
        Point(0, 0),
        Point(1, 0),
        Point(0, 1),
        Point(1, 1),
        Point(0, 2),
        Point(1, 2),
    ]  # Only 6 moves
    state = GameState(turns)
    assert state.status == GameStatus.UNDECIDED
    assert state.winner_parity is None


def test_win_and_winner():
    # Column-0 vertical win for player-0 after 7 moves
    turns = [
        Point(0, 0),
        Point(1, 0),
        Point(0, 1),
        Point(1, 1),
        Point(0, 2),
        Point(1, 2),
        Point(0, 3),  # 4 in column 0 (vertical win)
    ]
    state = GameState(turns)

    assert state.status == GameStatus.WIN
    assert state.winner_parity == 0  # odd number of turns → player_0 by spec


def test_draw(no_fours_pattern: list[Point]):
    # Fill the board completely: 7×7 = 49 moves — no connect-four pattern
    state = GameState(no_fours_pattern)

    assert state.status == GameStatus.DRAW
    assert state.winner_parity is None
