from abc import ABC, abstractmethod
from ssg.game.state import GameState
from ssg.models.player import Player
from ssg.utils import Point


class AIPlayer(Player, ABC):
    @classmethod
    @abstractmethod
    def play(cls, state: GameState) -> Point: ...
