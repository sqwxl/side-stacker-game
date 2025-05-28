from ssg.game.board import GameBoard
from ssg.game.engine import GameEngine, GameStatus
from ssg.utils import Point


class GameState:
    turns: list[Point]
    engine: GameEngine

    def __init__(self, turns: list[Point]) -> None:
        self.turns = turns
        self.engine = GameEngine(turns)

    @property
    def board(self) -> GameBoard:
        return self.engine.board

    @property
    def status(self) -> GameStatus:
        return self.engine.status

    @property
    def legal_cells(self) -> list[Point]:
        return self.engine.legal_cells

    @property
    def next_turn(self) -> int:
        return len(self.turns)

    @property
    def next_parity(self) -> int:
        return self.next_turn % 2

    @property
    def winner_parity(self) -> int | None:
        if self.status != GameStatus.WIN:
            return None
        return (len(self.turns) - 1) % 2
