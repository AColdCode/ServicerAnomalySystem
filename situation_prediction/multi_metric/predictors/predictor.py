import os
import torch
import numpy as np
import pandas as pd

from situation_prediction.multi_metric.models.lstm_predictor import MultiMetricLSTM
from situation_prediction.multi_metric.utils.model_manager import ModelManager
from situation_prediction.multi_metric.config import *


class MultiMetricPredictor:
    """
    多指标态势预测器
    """

    def __init__(self):

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        print("预测设备:", self.device)

        self.model = MultiMetricLSTM(
            input_size=INPUT_SIZE,
            hidden_size=HIDDEN_SIZE,
            num_layers=NUM_LAYERS,
            pred_len=PRED_LENGTH
        ).to(self.device)

    # =========================================================
    # 加载模型
    # =========================================================
    def load_model(self, server_name):

        model_path = os.path.join(MODEL_DIR, f"{server_name}_lstm.pth")

        if not os.path.exists(model_path):

            raise Exception(f"模型不存在: {model_path}")

        ModelManager.load(self.model, model_path)

        print("模型加载:", model_path)

    # =========================================================
    # 滑动窗口预测
    # =========================================================
    def predict_dataframe(self, df):

        data = df[FEATURE_COLUMNS].values

        timestamps = df["timestamp"].values

        seq_len = SEQ_LENGTH

        preds = []

        real = []

        pred_timestamps = []

        self.model.eval()

        with torch.no_grad():

            for i in range(seq_len, len(data)):

                window = data[i - seq_len:i]

                x = torch.tensor(window, dtype=torch.float32)

                x = x.unsqueeze(0).to(self.device)

                pred = self.model(x)

                pred = pred.cpu().numpy()[0][0]

                preds.append(pred)

                real.append(data[i])

                pred_timestamps.append(timestamps[i])

        preds = np.array(preds)

        real = np.array(real)

        result_df = self._build_result_df(
            pred_timestamps,
            real,
            preds
        )

        return result_df

    # =========================================================
    # 构建结果DataFrame
    # =========================================================
    def _build_result_df(self, timestamps, real, pred):

        result = pd.DataFrame()

        result["timestamp"] = timestamps

        for i, col in enumerate(FEATURE_COLUMNS):

            result[f"real_{col}"] = real[:, i]

            result[f"pred_{col}"] = pred[:, i]

        return result
    