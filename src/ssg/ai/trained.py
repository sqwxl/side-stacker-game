from typing import override
import torch

from ssg.ai.ai_player import AIPlayer
from ssg.ai.heuristic import HeuristicAI
from ssg.ai.training.nn import StateValueNet
from ssg.ai.training.simulation import extract_features
from ssg.game.engine import GameStatus
from ssg.game.state import GameState
from ssg.utils import Point

model = StateValueNet()
try:
    model.load_state_dict(
        torch.load("artifacts/side_stacker_value_net.pth", map_location="cpu")
    )
except FileNotFoundError as e:
    print(f"Model weight data not found: {e}")
    model.eval()  # set to eval mode


class TrainedAI(AIPlayer):
    @override
    @classmethod
    def play(cls, state: GameState) -> Point:
        if state.status != GameStatus.UNDECIDED:
            raise Exception("Cannot play move, game is already finished.")

        parity = state.next_parity

        legal_moves = state.legal_cells

        if len(legal_moves) == 1:
            return legal_moves[0]

        best_move = None
        best_value = -float("inf")

        # First run through to find a winning move
        for cell in legal_moves:
            # Play here immediately if it results in a win
            if GameState(state.turns + [cell]).status == GameStatus.WIN:
                return cell

        for cell in legal_moves:
            # Simulate the outcome of letting the opponent play here
            # and play here immediately if it blocks the opponents win
            elsewhere = next(c for c in legal_moves if c != cell)
            if GameState(state.turns + [elsewhere, cell]).status == GameStatus.WIN:
                return cell

            # Extract features for the new state from current player's perspective
            features = extract_features(GameState(state.turns + [cell]), parity)

            # Model expects a batch tensor; add batch dimension and evaluate
            state_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0)

            value = model(state_tensor).item()

            # Flip value since it's now opponent's turn in new_state
            move_value = -value
            if move_value > best_value:
                best_value = move_value
                best_move = cell

        # If no move found (shouldn't happen as game not finished), fallback to Heuristic
        return best_move if best_move is not None else HeuristicAI.play(state)
