from dataclasses import dataclass

from ssg.constants import COLS, DIRECTIONS, ROWS
from ssg.game.state import GameState
from ssg.utils import Point


@dataclass(frozen=True)
class Candidate:
    point: Point
    value: int


def get_candidates(state: GameState) -> tuple[list[Candidate], list[Candidate]]:
    even: list[Candidate] = []
    odd: list[Candidate] = []

    for point in state.legal_cells:
        value = _cell_value(state, point)

        even.append(Candidate(point=point, value=value[0]))
        odd.append(Candidate(point=point, value=value[1]))

    return (even, odd)


def _cell_value(
    state: GameState,
    point: Point,
) -> tuple[int, int]:
    max_even = 0
    max_odd = 0

    for dx, dy in DIRECTIONS:
        even_streak = odd_streak = 0
        for k in [-1, 1]:
            e = o = 0
            c, r = point
            while True:
                c += dx * k
                r += dy * k

                if c < 0 or c >= COLS or r < 0 or r >= ROWS:
                    break

                if state.board.is_free(c, r):
                    break

                parity = state.board[r][c] % 2

                if parity == 0:
                    if o > 0:
                        break
                    e += 1
                elif parity == 1:
                    if e > 0:
                        break
                    o += 1
            even_streak += e
            odd_streak += o

        if even_streak > max_even:
            max_even = even_streak
        if odd_streak > max_odd:
            max_odd = odd_streak

    return (max_even, max_odd)
