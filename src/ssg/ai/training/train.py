import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

from ssg.ai.random import RandomAI
from ssg.ai.heuristic import HeuristicAI
from ssg.ai.trained import TrainedAI
from ssg.ai.training.simulation import simulate_game
from ssg.ai.training.nn import StateValueNet


NUM_GAMES = 10_000
EPOCHS = 15


def main():
    player_A = HeuristicAI
    player_B = TrainedAI

    X: list[list[float]] = []
    y: list[float] = []

    # Simulate games
    for i in range(NUM_GAMES):
        features, targets = simulate_game(player_A, player_B)
        X.extend(features)
        y.extend(targets)
        if i % (NUM_GAMES // 100) == 0:
            p = 100 * i // NUM_GAMES
            print(
                f"Running {NUM_GAMES} game simulations: {p:>3}%", end="\r", flush=True
            )

    # Convert to tensors
    X_tensor = torch.tensor(X, dtype=torch.float32)  # (N, 49)
    y_tensor = torch.tensor(y, dtype=torch.float32).unsqueeze(1)  # (N, 1)

    dataset = TensorDataset(X_tensor, y_tensor)
    dataloader = DataLoader(dataset, batch_size=512, shuffle=True)

    # Set up the model, optimiser, loss
    model = StateValueNet()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-3)

    # Training loop
    model.train()
    for epoch in range(1, EPOCHS + 1):
        running_loss = 0.0
        for xb, yb in dataloader:
            pred = model(xb)
            loss = criterion(pred, yb)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * xb.size(0)
        epoch_loss = running_loss / len(dataset)
        print(f"epoch {epoch:02d}   loss {epoch_loss:.4f}")

    torch.save(model.state_dict(), "artifacts/side_stacker_value_net.pth")


if __name__ == "__main__":
    main()
