import pytest
from sqlite3 import Connection

from ssg.models.player import Player


def test_create_player(db: Connection):
    player = Player.create(db, "token123")
    assert player.id is not None
    assert player.token == "token123"


def test_load_existing_player(db: Connection):
    created = Player.create(db, "abc")
    loaded = Player.load(db, "abc")

    assert loaded is not None
    assert created == loaded


def test_load_nonexistent_player_returns_none(db: Connection):
    assert Player.load(db, "nonexistent") is None


def test_get_or_create_loads_existing(db: Connection):
    p1 = Player.create(db, "x")
    p2 = Player.get_or_create(db, "x")

    assert p1 == p2


def test_get_or_create_creates_new(db: Connection):
    p = Player.get_or_create(db, "newtoken")
    assert p is not None
    assert p.token == "newtoken"


def test_create_empty_token_raises(db: Connection):
    with pytest.raises(ValueError):
        Player.create(db, "")


def test_eq_operator(db: Connection):
    p1 = Player.create(db, "equal_token")
    p2 = Player.load(db, "equal_token")
    p3 = Player.create(db, "other_token")

    assert p1 == p2
    assert p1 != p3
