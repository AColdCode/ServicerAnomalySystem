import torch
import numpy as np
import pandas as pd
import os

from situation_prediction.multi_metric.models.attention_lstm import AttentionLSTM
from situation_prediction.multi_metric.utils.model_manager import ModelManager
from situation_prediction.multi_metric.config import *


class AttentionPredictor:

    def __init__(self):

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model = AttentionLSTM(
            INPUT_SIZE,
            HIDDEN_SIZE,
            NUM_LAYERS,
            PRED_LENGTH
        ).to(self.device)

    def load_model(self, server):

        path = os.path.join(
            MODEL_DIR,
            f"{server}_attention_lstm.pth"
        )

        ModelManager.load(self.model, path)

        print("模型加载:", path)

    def predict(self, df):

        data = df[FEATURE_COLUMNS].values

        timestamps = df["timestamp"].values

        preds = []

        real = []

        times = []

        self.model.eval()

        with torch.no_grad():

            for i in range(SEQ_LENGTH, len(data)):

                window = data[i-SEQ_LENGTH:i]

                x = torch.tensor(window, dtype=torch.float32)

                x = x.unsqueeze(0).to(self.device)

                pred, _ = self.model(x)

                pred = pred.cpu().numpy()[0][0]

                preds.append(pred)

                real.append(data[i])

                times.append(timestamps[i])

        preds = np.array(preds)

        real = np.array(real)

        result = pd.DataFrame()

        result["timestamp"] = times

        for i, col in enumerate(FEATURE_COLUMNS):

            result[f"real_{col}"] = real[:, i]

            result[f"pred_{col}"] = preds[:, i]

        return result
    