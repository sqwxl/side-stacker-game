from itertools import chain, tee, zip_longest

import pytest

from ssg.game.board import GameBoard
from ssg.utils import Point
from ssg import app, init_db


@pytest.fixture(autouse=True)
def db(tmpdir: str):
    app.config["DATABASE"] = str(tmpdir.join("blog.db"))
    db = init_db()

    yield db

    db.close()


@pytest.fixture
def no_fours_pattern() -> list[Point]:
    cols, rows = GameBoard.cols, GameBoard.rows

    pattern = (
        ((c + r // 2) % 2, Point(c, r)) for c in range(cols) for r in range(rows)
    )
    # Produces the following:
    # ⚪⚫⚪⚫⚪⚫⚪
    # ⚪⚫⚪⚫⚪⚫⚪
    # ⚫⚪⚫⚪⚫⚪⚫
    # ⚫⚪⚫⚪⚫⚪⚫
    # ⚪⚫⚪⚫⚪⚫⚪
    # ⚪⚫⚪⚫⚪⚫⚪
    # ⚫⚪⚫⚪⚫⚪⚫

    b1, b2 = tee(pattern)

    zeros = [p for z, p in b1 if z == 0]
    ones = [p for o, p in b2 if o == 1]

    return list(
        p
        for p in chain.from_iterable(zip_longest(zeros, ones, fillvalue=None))
        if p is not None
    )
