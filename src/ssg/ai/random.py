from random import choice

from ssg.ai.ai_player import AIPlayer
from ssg.game.state import GameState
from ssg.utils import Point


class RandomAI(AIPlayer):
    @classmethod
    def play(cls, state: GameState) -> Point:
        return choice(state.legal_cells)
