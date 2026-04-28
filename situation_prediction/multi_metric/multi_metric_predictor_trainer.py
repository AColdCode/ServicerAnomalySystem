import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

from data_source.db_reader import DBReader
from preprocessing.preprocessor import TimeSeriesPreprocessor

from situation_prediction.multi_metric.models.lstm_predictor import MultiMetricLSTM
from situation_prediction.multi_metric.models.multi_metric_attention_lstm import MultiMetricAttentionLSTM
from situation_prediction.multi_metric.utils.model_manager import ModelManager

from situation_prediction.multi_metric.scaler.multi_standard_scaler import MultiStandardScaler
from situation_prediction.multi_metric.scaler.multi_scaler_manager import MultiScalerManager


class MultiMetricPredictorTrainer:

    def __init__(
        self,
        db_path,
        table_name,
        pred_steps_list=(288, ),  # 1h,6h,24h
        window_size=30,
        epochs=15,
        batch_size=32,
        lr=0.001
    ):
        self.db_path = db_path
        self.table_name = table_name
        self.pred_steps_list = pred_steps_list

        self.window_size = window_size
        self.epochs = epochs
        self.batch_size = batch_size
        self.lr = lr

        self.metrics = [
            "cpu_usage", "response_time", "memory_usage",
            "disk_usage", "io_read", "io_write",
            "service_rt", "service_qps"
        ]

        self.reader = DBReader(db_path)
        self.processor = TimeSeriesPreprocessor()

        self.model_manager = ModelManager()
        self.scaler_manager = MultiScalerManager()

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 时间特征
    def _add_time_features(self, df):

        df["timestamp"] = pd.to_datetime(df["timestamp"])

        hour = df["timestamp"].dt.hour

        df["sin_hour"] = np.sin(2 * np.pi * hour / 24)
        df["cos_hour"] = np.cos(2 * np.pi * hour / 24)

        return df

    # 预处理（核心）
    def _preprocess(self, df):

        df = self.processor.process(df)
        df = self._add_time_features(df)

        raw = df[self.metrics].values

        # 差分
        diff = raw[1:] - raw[:-1]
        raw = raw[1:]

        time_feat = df[["sin_hour", "cos_hour"]].values[1:]

        # 拼接
        data = np.concatenate([raw, diff, time_feat], axis=1)  # 8 + 8 + 2 = 18维

        # scaler（多维）
        scaler = MultiStandardScaler()
        scaler.fit(data)

        data_norm = scaler.transform(data)

        # 保存 scaler
        self.scaler_manager.save(scaler, self.table_name)

        return data_norm

    # 构建数据集
    def _build_dataset(self, data, steps):

        X, y = [], []

        for i in range(len(data) - self.window_size - steps):

            X.append(data[i:i + self.window_size])

            # 只预测前8维（真实指标）
            y.append(data[i + self.window_size:i + self.window_size + steps, :len(self.metrics)])

        X = torch.tensor(np.array(X), dtype=torch.float32)
        y = torch.tensor(np.array(y), dtype=torch.float32)

        return DataLoader(
            TensorDataset(X, y),
            batch_size=self.batch_size,
            shuffle=True
        )

    # 训练
    def train_and_save(self):

        df = self.reader.read_server_metrics(self.table_name)

        data = self._preprocess(df)
        return

        for steps in self.pred_steps_list:

            print(f"\n[训练] {self.table_name} → {steps} steps")

            loader = self._build_dataset(data, steps)

            model = MultiMetricAttentionLSTM(
                input_size=data.shape[1],
                hidden_size=128,
                num_layers=2,
                pred_len=steps,
                output_size=len(self.metrics)
            ).to(self.device)

            optimizer = optim.Adam(model.parameters(), lr=self.lr)
            criterion = nn.SmoothL1Loss()

            for epoch in range(self.epochs):

                total_loss = 0

                for batch_x, batch_y in loader:

                    batch_x = batch_x.to(self.device)
                    batch_y = batch_y.to(self.device)

                    optimizer.zero_grad()

                    pred = model(batch_x)

                    loss = criterion(pred, batch_y)

                    loss.backward()
                    optimizer.step()

                    total_loss += loss.item()

                print(f"Epoch {epoch+1}/{self.epochs} Loss={total_loss/len(loader):.6f}")

            model_name = f"{steps}_model.pth"
            path = os.path.join("multi_models", model_name)

            self.model_manager.save(model, path)

            print(f"模型保存: {model_name}")


if __name__ == "__main__":
    service = MultiMetricPredictorTrainer(
        r"D:\Python\pythonProject\ServicerAnomalySystem\data_generator\metrics.db",
        "server_01_metrics"
    )
    service.train_and_save()
