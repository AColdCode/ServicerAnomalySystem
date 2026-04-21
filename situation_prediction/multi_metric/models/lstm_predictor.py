import torch
import torch.nn as nn


class MultiMetricLSTM(nn.Module):

    def __init__(self, input_size, hidden_size, num_layers, pred_len, output_size):

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

        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        batch_size = x.size(0)

        _, (h, c) = self.lstm(x)

        decoder_input = torch.zeros(batch_size, 1, self.output_size).to(x.device)

        outputs = []

        for _ in range(self.pred_len):
            out, (h, c) = self.decoder_lstm(decoder_input, (h, c))

            step_out = self.fc(out[:, -1, :])

            outputs.append(step_out.unsqueeze(1))

            decoder_input = step_out.unsqueeze(1)

        return torch.cat(outputs, dim=1)
    