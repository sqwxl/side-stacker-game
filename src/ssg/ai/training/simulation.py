from ssg.ai.ai_player import AIPlayer
from ssg.game.engine import GameStatus
from ssg.game.state import GameState
from ssg.utils import Point


def simulate_game(player_0: type[AIPlayer], player_1: type[AIPlayer]):
    turns: list[Point] = []

    state = GameState(turns)

    current_player = player_0

    game_states: list[list[float]] = []

    while state.status == GameStatus.UNDECIDED:
        # Choose a move according to the current player's policy:
        point = current_player.play(state)

        # Record current state features for training (before making the move)
        game_states.append(extract_features(state, state.next_parity))

        turns.append(point)
        state = GameState(turns)

        # Swap player turn
        current_player = player_1 if current_player == player_0 else player_0

    # Game ended: determine outcome for each state from perspective of the player who was about to move
    result = state.status  # "win", "draw", or "undecided"
    winner = (
        state.engine.board[state.turns[-1]] % 2 if result == GameStatus.WIN else None
    )

    # Assign reward values: +1 for win, -1 for loss, 0 for draw, from each player's perspective
    outcomes: list[float] = []
    for i, _ in enumerate(game_states):
        parity = i % 2

        if result == GameStatus.WIN:
            outcomes.append(1.0 if parity == winner else -1.0)
        elif result == GameStatus.DRAW:
            outcomes.append(0.0)

    return game_states, outcomes


def extract_features(state: GameState, parity: int) -> list[float]:
    """
    Return a COLS*ROWS-length vector with cells encoded as
        +1  piece of the side to move
        -1  opponent piece
         0  empty
    """
    features: list[float] = []

    for row in state.board:
        for val in row:
            if val == -1:
                features.append(0.0)
            else:
                features.append(1.0 if parity == val % 2 else -1.0)

    return features
