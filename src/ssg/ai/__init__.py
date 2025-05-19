from enum import IntEnum

from ssg.ai.heuristic import HeuristicAI
from ssg.ai.random import RandomAI
from ssg.ai.trained import TrainedAI


class AIPlayerID(IntEnum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


AIPlayerMap = {
    AIPlayerID.EASY: RandomAI,
    AIPlayerID.MEDIUM: HeuristicAI,
    AIPlayerID.HARD: TrainedAI,
}
