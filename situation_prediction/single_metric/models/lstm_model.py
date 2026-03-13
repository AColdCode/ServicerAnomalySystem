import torch
import torch.nn as nn


class LSTMModel(nn.Module):
    """
    LSTM时间序列预测模型
    """

    def __init__(self, input_size=1, hidden_size=64, num_layers=2):

        super(LSTMModel, self).__init__()

        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True
        )

        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):

        out, _ = self.lstm(x)

        out = out[:, -1, :]

        out = self.fc(out)

        return out