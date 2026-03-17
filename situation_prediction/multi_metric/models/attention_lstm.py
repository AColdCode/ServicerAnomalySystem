import torch
import torch.nn as nn


class AttentionLayer(nn.Module):
    """
    时间注意力层
    """

    def __init__(self, hidden_size):

        super().__init__()

        self.W = nn.Linear(hidden_size, hidden_size)

        self.v = nn.Linear(hidden_size, 1)

    def forward(self, lstm_output):

        # lstm_output
        # [batch, seq_len, hidden]

        score = torch.tanh(self.W(lstm_output))

        attention_weights = torch.softmax(self.v(score), dim=1)

        context = torch.sum(attention_weights * lstm_output, dim=1)

        return context, attention_weights


class AttentionLSTM(nn.Module):

    """
    Attention-LSTM 多指标预测模型
    """

    def __init__(
        self,
        input_size,
        hidden_size,
        num_layers,
        pred_len,
        dropout=0.2
    ):

        super().__init__()

        self.pred_len = pred_len

        self.lstm = nn.LSTM(
            input_size,
            hidden_size,
            num_layers,
            batch_first=True,
            dropout=dropout
        )

        self.attention = AttentionLayer(hidden_size)

        self.fc = nn.Sequential(

            nn.Linear(hidden_size, hidden_size),

            nn.ReLU(),

            nn.Linear(hidden_size, input_size)
        )

    def forward(self, x):

        # x
        # [batch, seq_len, features]

        lstm_out, _ = self.lstm(x)

        context, attn = self.attention(lstm_out)

        outputs = []

        h = context

        for _ in range(self.pred_len):

            y = self.fc(h)

            outputs.append(y)

        outputs = torch.stack(outputs, dim=1)

        return outputs, attn
    