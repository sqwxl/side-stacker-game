from typing import override
from ssg.ai.ai_player import AIPlayer
from ssg.ai.analysis import Candidate, get_candidates
from ssg.game.state import GameState
from ssg.utils import Point


class HeuristicAI(AIPlayer):
    """
    General strategy:
        1. Look at existing moves for candidate moves
            A candidate is a group of one or more cells
            of the same color that have enough free spots
            on either end to connect four.
        2. If it is possible to play a winning move, play it.
        3. If it is possible to prevent the opponent from making
           a winning move, play there.
        4. Otherwise, play to form the longest line possible.
        5. Ties are broken at random.
        6. If there are no candidates, play at random.
    """

    @override
    @classmethod
    def play(cls, state: GameState) -> Point:
        parity = state.next_parity

        candidates = get_candidates(state)

        own = cls._choose_candidate(candidates[parity])
        adv = cls._choose_candidate(candidates[(parity + 1) % 2])

        return (
            own.point
            if own.value >= adv.value  # build > block
            else adv.point
        )

    @classmethod
    def _choose_candidate(cls, candidates: list[Candidate]) -> Candidate:
        hi = candidates[0]
        for c in candidates:
            if c.value == 3:  # win/block win
                return c
            if c.value > hi.value:
                hi = c

        return hi
