import torch
import torch.nn as nn


class MultiMetricAttentionLSTM(nn.Module):

    def __init__(
        self,
        input_size,
        hidden_size,
        num_layers,
        pred_len,
        output_size
    ):
        super().__init__()

        self.hidden_size = hidden_size
        self.pred_len = pred_len
        self.output_size = output_size

        # =========================
        # Encoder
        # =========================
        self.encoder = nn.LSTM(
            input_size,
            hidden_size,
            num_layers,
            batch_first=True
        )

        # =========================
        # Attention
        # =========================
        self.attn = nn.Linear(hidden_size, hidden_size)
        self.v = nn.Linear(hidden_size, 1, bias=False)

        # =========================
        # Decoder
        # =========================
        self.decoder = nn.LSTM(
            input_size=output_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True
        )

        # 输出层
        self.fc = nn.Linear(hidden_size, output_size)

    # =========================================================
    # Attention
    # =========================================================
    def _attention(self, encoder_outputs, hidden):

        # encoder_outputs: (B, T, H)
        # hidden: (B, H)

        hidden = hidden.unsqueeze(1).repeat(1, encoder_outputs.size(1), 1)

        energy = torch.tanh(self.attn(encoder_outputs) + hidden)

        scores = self.v(energy).squeeze(-1)  # (B, T)

        weights = torch.softmax(scores, dim=1)  # (B, T)

        context = torch.bmm(weights.unsqueeze(1), encoder_outputs)
        # (B,1,H)

        return context

    # =========================================================
    # forward
    # =========================================================
    def forward(self, x):

        batch_size = x.size(0)

        # =========================
        # Encoder
        # =========================
        encoder_outputs, (h, c) = self.encoder(x)

        # =========================
        # Decoder
        # =========================
        decoder_input = torch.zeros(
            batch_size, 1, self.output_size
        ).to(x.device)

        outputs = []

        for _ in range(self.pred_len):

            # attention context
            context = self._attention(
                encoder_outputs,
                h[-1]
            )

            # 拼接 context + decoder input
            decoder_in = decoder_input

            out, (h, c) = self.decoder(decoder_in, (h, c))

            out = self.fc(out[:, -1, :])  # (B, output)

            outputs.append(out.unsqueeze(1))

            decoder_input = out.unsqueeze(1)

        return torch.cat(outputs, dim=1)
