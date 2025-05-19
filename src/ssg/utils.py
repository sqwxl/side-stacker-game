from typing import NamedTuple, override


class Point(NamedTuple):
    col: int
    row: int

    @override
    def __eq__(self, other: object):
        if not isinstance(other, Point):
            return NotImplemented

        return self.col == other.col and self.row == other.row


def clamp_int(val: int, lo: int, hi: int) -> int:
    if val < lo:
        return lo

    if hi < val:
        return hi

    return val
