import torch
import torch.nn as nn


class MultiMetricLSTM(nn.Module):

    def __init__(self, input_size, hidden_size, num_layers, pred_len):

        super(MultiMetricLSTM, self).__init__()

        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.pred_len = pred_len

        self.lstm = nn.LSTM(
            input_size,
            hidden_size,
            num_layers,
            batch_first=True
        )

        self.fc = nn.Linear(hidden_size, input_size)

    def forward(self, x):

        # x shape
        # [batch, seq_len, features]

        out, _ = self.lstm(x)

        last_hidden = out[:, -1, :]

        preds = []

        h = last_hidden

        for _ in range(self.pred_len):

            y = self.fc(h)

            preds.append(y)

        preds = torch.stack(preds, dim=1)

        return preds
    