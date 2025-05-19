from typing import ClassVar, overload, override

from ssg.constants import COLS, ROWS
from ssg.utils import Point


class GameBoard:
    """
    Represents a game record as 2-D matrix of integers.
    Empty cells have value -1. Played cells have the turn at which they occur.
    """

    cols: ClassVar[int] = COLS
    rows: ClassVar[int] = ROWS
    board: list[list[int]]
    turns: list[Point]

    def __init__(self, turns: list[Point]):
        self.board = [[-1 for _ in range(self.cols)] for _ in range(self.rows)]
        self.turns = turns

        for i, (col, row) in enumerate(turns):
            if self[row][col] != -1:
                raise ValueError(f"Duplicate game move: {col},{row}")

            self[row][col] = i

    @override
    def __str__(self):
        symbols = {-1: "⚫", 0: "🔴", 1: "🔵"}
        return (
            "\n"
            + "\n".join(
                "".join(symbols[c if c < 0 else c % 2] for c in row)
                for row in self.board
            )
            + "\n"
        )

    def __iter__(self):
        return iter(self.board)

    @overload
    def __getitem__(self, v: int) -> list[int]: ...
    @overload
    def __getitem__(self, v: Point) -> int: ...
    def __getitem__(self, v: int | Point):
        if isinstance(v, Point):
            return self.board[v.row][v.col]
        return self.board[v]

    def is_free(self, col: int, row: int) -> bool:
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False

        return self[row][col] < 0
