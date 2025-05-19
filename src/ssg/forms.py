from enum import IntEnum, StrEnum
from random import choice
from sqlite3 import Connection
from typing import cast

from werkzeug.datastructures import MultiDict

from ssg.ai import AIPlayerID
from ssg.models.game import Game


class Color(StrEnum):
    RANDOM = "random"
    RED = "red"
    BLUE = "blue"


class GameStyle(StrEnum):
    LOCAL = "local"
    REMOTE = "remote"
    AI = "ai"
    AI_VS_AI = "ai-vs-ai"


class Difficulty(IntEnum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


class GameForm:
    player_0: int | None
    player_1: int | None

    def __init__(self, player_id: int, form: MultiDict[str, str]) -> None:
        game_style = cast(GameStyle, form["game-style"])

        if game_style == GameStyle.LOCAL:
            self.player_0 = self.player_1 = player_id
            return

        difficulty = cast(Difficulty, int(form["difficulty"]))
        ai_player_id = AIPlayerID(difficulty)

        if game_style == GameStyle.AI_VS_AI:
            self.player_0 = self.player_1 = ai_player_id
            return

        color = cast(Color, form["color"])
        if color == Color.RANDOM:
            color = choice([Color.RED, Color.BLUE])

        if color == Color.RED:
            self.player_0 = player_id
            self.player_1 = ai_player_id if game_style == GameStyle.AI else None
        else:
            self.player_0 = ai_player_id if game_style == GameStyle.AI else None
            self.player_1 = player_id

    def save(self, db: Connection) -> Game:
        return Game.create(db, player_0=self.player_0, player_1=self.player_1)
