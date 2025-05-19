import torch.nn as nn

from ssg.constants import COLS, ROWS


class StateValueNet(nn.Module):
    def __init__(self):
        super(StateValueNet, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(COLS * ROWS, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 1),  # single output for state value
        )

    def forward(self, x):
        # x is expected shape (batch, 49)
        return self.layers(x)
