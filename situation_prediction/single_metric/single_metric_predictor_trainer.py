import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

from data_source.db_reader import DBReader
from preprocessing.preprocessor import TimeSeriesPreprocessor

from situation_prediction.single_metric.models.lstm_model import LSTMModel
from situation_prediction.single_metric.utils.model_manager import ModelManager
from situation_prediction.single_metric.scaler.scaler_manager import ScalerManager
from situation_prediction.single_metric.scaler.standard_scaler import StandardScaler


class SingleMetricPredictorTrainer:

    def __init__(
        self,
        db_path,
        table_name,
        metric,
        window_size=30,
        output_steps=12,
        epochs=30,
        batch_size=64,
        lr=0.001
    ):
        self.db_path = db_path
        self.table_name = table_name
        self.metric = metric

        self.window_size = window_size
        self.output_steps = output_steps

        self.epochs = epochs
        self.batch_size = batch_size
        self.lr = lr

        self.model_name = f"{metric}_{output_steps}_model"

        self.reader = DBReader(self.db_path)
        self.processor = TimeSeriesPreprocessor()
        self.manager = ModelManager()
        self.scaler = StandardScaler()
        self.scaler_manager = ScalerManager()

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 数据加载
    def _load_data(self):
        return self.reader.read_server_metrics(self.table_name)

    # 差分 + 标准化
    def _preprocess(self, df):
        df = self.processor.process(df)

        values = df[self.metric].values

        # 一阶差分
        diff = values[1:] - values[:-1]

        # 标准化
        self.scaler.fit(diff)
        diff_norm = self.scaler.transform(diff)

        self.scaler_manager.save(self.scaler, self.table_name, self.metric)

        return diff_norm

    # 构建数据
    def _build_dataset(self, diff):
        X, y = [], []

        for i in range(len(diff) - self.window_size - self.output_steps):
            X.append(diff[i:i + self.window_size])
            y.append(diff[i + self.window_size:i + self.window_size + self.output_steps])

        X = np.array(X, dtype=np.float32)
        y = np.array(y, dtype=np.float32)

        X = torch.from_numpy(X).unsqueeze(-1)  # (N, window, 1)
        y = torch.from_numpy(y)  # (N, steps)

        loader = DataLoader(
            TensorDataset(X, y),
            batch_size=self.batch_size,
            shuffle=True,
            pin_memory=True
        )

        return loader

    # 训练
    def train_and_save(self):
        intervals = {
            "1h": 12,
            "6h": 72,
            "24h": 288
        }
        for _, steps in intervals.items():
            self.output_steps = steps
            self.model_name = f"{self.metric}_{steps}_model"
            print(f"[训练] {self.metric} → {self.output_steps} steps")

            df = self._load_data()
            diff = self._preprocess(df)
            loader = self._build_dataset(diff)

            model = LSTMModel(output_steps=self.output_steps).to(self.device)
            optimizer = optim.Adam(model.parameters(), lr=self.lr)
            criterion = nn.MSELoss()

            for epoch in range(self.epochs):
                total_loss = 0

                for batch_x, batch_y in loader:
                    batch_x = batch_x.to(self.device)
                    batch_y = batch_y.to(self.device)

                    optimizer.zero_grad()

                    out = model(batch_x)

                    loss = criterion(out, batch_y)
                    loss.backward()
                    optimizer.step()

                    total_loss += loss.item()

                print(f"Epoch {epoch+1}/{self.epochs} Loss={total_loss/len(loader):.6f}")

            self.manager.save(model, self.table_name, self.model_name)

            print(f"模型保存: {self.model_name}")


if __name__ == "__main__":
    db_path = r"D:\Python\pythonProject\ServicerAnomalySystem\data_generator\metrics.db"
    table = "server_01_metrics"
    metric = "io_read"

    trainer = SingleMetricPredictorTrainer(
        db_path=db_path,
        table_name=table,
        metric=metric,
        window_size=30,
        epochs=30
    )

    trainer.train_and_save()
