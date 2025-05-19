from enum import StrEnum

from ssg.constants import DIRECTIONS, COLS, ROWS
from ssg.game.board import GameBoard
from ssg.utils import Point


def _get_win_lines(col: int, row: int) -> list[list[Point]]:
    lines: list[list[Point]] = []

    for dx, dy in DIRECTIONS:
        line: list[Point] = []
        for k in range(-3, 4):  # window of 7 cells
            c, r = col + k * dx, row + k * dy
            if 0 <= c < COLS and 0 <= r < ROWS:
                line.append(Point(c, r))
        lines.append(line)

    return lines


WIN_LINES: dict[Point, list[list[Point]]] = {}
for c in range(COLS):
    for r in range(ROWS):
        WIN_LINES[Point(c, r)] = _get_win_lines(c, r)


class GameStatus(StrEnum):
    UNDECIDED = "undecided"
    WIN = "win"
    DRAW = "draw"


class GameEngine:
    turns: list[Point]
    board: GameBoard
    _status: GameStatus | None = None
    _legal_cells: list[Point] | None = None

    def __init__(self, turns: list[Point]) -> None:
        self.turns = turns
        self.board = GameBoard(turns)

    @property
    def status(self):
        if self._status is None:
            self._status = self._get_status()

        return self._status

    @property
    def legal_cells(self):
        if self._legal_cells is None:
            self._legal_cells = self._get_legal_cells()

        return self._legal_cells

    def _get_status(self) -> GameStatus:
        # A minimum of 7 turns is required for a player to connect four.
        if len(self.turns) < 7:
            return GameStatus.UNDECIDED

        point = self.turns[-1]

        lines = WIN_LINES[point]

        # print(self._debug_print_lines(*point, lines))

        parity = self.board[point] % 2

        for line in lines:
            if self._connect_four(parity, line):
                return GameStatus.WIN

        if len(self.turns) == self.board.rows * self.board.cols:
            return GameStatus.DRAW

        return GameStatus.UNDECIDED

    def _get_legal_cells(self) -> list[Point]:
        result: list[Point] = []
        cols, rows = self.board.cols, self.board.rows

        for r in range(rows):
            left = next((c for c in range(cols) if self.board.is_free(c, r)), None)

            if left is None:
                continue

            right = next((c for c in reversed(range(cols)) if self.board.is_free(c, r)))

            result.append(Point(left, r))

            if left != right:
                result.append(Point(right, r))

        return result

    def _connect_four(self, parity: int, line: list[Point]) -> bool:
        streak = 0

        for point in line:
            turn = self.board[point]

            if turn >= 0 and turn % 2 == parity:
                streak += 1
                if streak == 4:
                    return True
            else:
                streak = 0

        return False

    def _debug_print_lines(self, col: int, row: int, lines: list[list[Point]]) -> str:
        g = [["⚫" for _ in range(self.board.cols)] for _ in range(self.board.rows)]

        for line in lines:
            for p in line:
                g[p[1]][p[0]] = "⭕"
        g[row][col] = "🔴"

        return "\n" + "\n".join("".join(row) for row in g) + "\n"
