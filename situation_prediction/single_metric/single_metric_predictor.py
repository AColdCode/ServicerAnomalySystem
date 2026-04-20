# single_metric_predictor.py

import torch
import numpy as np

from data_source.db_reader import DBReader
from preprocessing.preprocessor import TimeSeriesPreprocessor

from situation_prediction.single_metric.models.lstm_model import LSTMModel
from situation_prediction.single_metric.utils.model_manager import ModelManager
from situation_prediction.single_metric.scaler.scaler_manager import ScalerManager
from situation_prediction.single_metric.scaler.standard_scaler import StandardScaler


class SingleMetricPredictor:

    def __init__(self, metric, table_name, window_size=30, db_path="data_generator/metrics.db"):
        self.db_path = db_path
        self.table_name = table_name
        self.metric = metric
        self.window_size = window_size

        self.reader = DBReader(db_path)
        self.processor = TimeSeriesPreprocessor()

        self.manager = ModelManager()
        self.scaler_manager = ScalerManager()
        self.scaler = StandardScaler()

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def predict_future(self, hours=1, interval_minutes=5):

        steps = int(hours * 60 / interval_minutes)

        # 加载模型
        model_name = f"{self.metric}_{steps}_model"
        model = LSTMModel(output_steps=steps)
        model = self.manager.load(model, self.table_name, model_name)
        model.to(self.device)
        model.eval()

        # 加载 scaler
        state = self.scaler_manager.load(self.table_name, self.metric)
        self.scaler.load_state_dict(state)

        # 读取数据
        df = self.reader.read_server_metrics(self.table_name)
        df = self.processor.process(df)

        values = df[self.metric].values

        # 差分
        diff = values[1:] - values[:-1]

        # 标准化
        diff_norm = self.scaler.transform(diff)

        # 最后窗口
        last_window = diff_norm[-self.window_size:]

        x = torch.tensor(last_window, dtype=torch.float32)\
            .unsqueeze(0).unsqueeze(-1).to(self.device)

        with torch.no_grad():
            pred_diff_norm = model(x).cpu().numpy().flatten()

        # 反归一化
        pred_diff = self.scaler.inverse_transform(pred_diff_norm)
        pred_diff = np.clip(pred_diff, -5, 5)

        # 还原
        last_val = values[-1]
        future = []

        cur = last_val
        for d in pred_diff:
            cur += d
            future.append(cur)

        future = [float(x) for x in future]

        return future


if __name__ == "__main__":
    predictor = SingleMetricPredictor(
        "io_read",
        "server_01_metrics",
        30,
        r"D:\Python\pythonProject\ServicerAnomalySystem\data_generator\metrics.db"
    )
    data = predictor.predict_future(24)
    print(data)
