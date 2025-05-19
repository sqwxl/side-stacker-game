from typing import Final

from ssg.utils import Point

COLS: Final = 7
ROWS: Final = 7

DIRECTIONS: Final[list[tuple[int, int]]] = [
    (1, 0),  # Horizontal
    (0, 1),  # Vertical
    (1, 1),  # Northwest-Southeast
    (1, -1),  # Northeast-Southwest
]
