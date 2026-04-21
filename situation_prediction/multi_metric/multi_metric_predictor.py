import numpy as np
import pandas as pd
import torch

from data_source.db_reader import DBReader
from preprocessing.preprocessor import TimeSeriesPreprocessor

from situation_prediction.multi_metric.models.multi_metric_attention_lstm import MultiMetricAttentionLSTM
from situation_prediction.multi_metric.utils.model_manager import ModelManager

from situation_prediction.multi_metric.scaler.multi_standard_scaler import MultiStandardScaler
from situation_prediction.multi_metric.scaler.multi_scaler_manager import MultiScalerManager


class MultiMetricPredictor:

    def __init__(self, db_path, table_name, window_size=30, interval=300):

        self.db_path = db_path
        self.table_name = table_name
        self.window_size = window_size
        self.interval = interval

        self.metrics = [
            "cpu_usage", "response_time", "memory_usage",
            "disk_usage", "io_read", "io_write",
            "service_rt", "service_qps"
        ]

        self.reader = DBReader(db_path)
        self.processor = TimeSeriesPreprocessor()
        self.model_manager = ModelManager()

        self.scaler = MultiStandardScaler()
        self.scaler_manager = MultiScalerManager()

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def _add_time_features(self, df):
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        hour = df["timestamp"].dt.hour
        df["sin_hour"] = np.sin(2 * np.pi * hour / 24)
        df["cos_hour"] = np.cos(2 * np.pi * hour / 24)
        return df

    def _build_input(self, df):

        df = self.processor.process(df)
        df = self._add_time_features(df)

        raw = df[self.metrics].values

        diff = raw[1:] - raw[:-1]
        raw = raw[1:]

        time_feat = df[["sin_hour", "cos_hour"]].values[1:]

        data = np.concatenate([raw, diff, time_feat], axis=1)

        data_norm = self.scaler.transform(data)

        return data_norm, raw, df

    def _load_model(self, steps):

        model = MultiMetricAttentionLSTM(
            input_size=18,
            hidden_size=128,
            num_layers=2,
            pred_len=steps,
            output_size=8
        )

        path = f"multi_models/{steps}_model.pth"
        model = self.model_manager.load(model, path)

        model.to(self.device)
        model.eval()

        return model

    def _load_scaler(self):
        state = self.scaler_manager.load(self.table_name)
        self.scaler.load_state_dict(state)

    def _predict(self, hours):

        steps = int(hours * 3600 / self.interval)

        model = self._load_model(steps)
        self._load_scaler()

        df = self.reader.read_server_metrics(self.table_name)

        data_norm, raw, df = self._build_input(df)

        last_window = data_norm[-self.window_size:]

        x = torch.tensor(last_window, dtype=torch.float32)\
            .unsqueeze(0).to(self.device)

        with torch.no_grad():
            pred_norm = model(x).cpu().numpy()[0]

        tmp = np.zeros((pred_norm.shape[0], self.scaler.mean.shape[0]))
        tmp[:, :8] = pred_norm

        pred = self.scaler.inverse_transform(tmp)[:, :8]

        pred = np.clip(pred, 0, None)

        return pred, raw, df

    def _calc_volatility(self, pred):
        return np.mean(np.abs(np.diff(pred, axis=0)))

    def _calc_smoothness(self, pred):
        return np.mean(np.var(np.diff(pred, axis=0), axis=0))

    def _calc_trend(self, pred):

        # 每个指标趋势
        slopes = []

        x = np.arange(len(pred))

        for i in range(pred.shape[1]):
            y = pred[:, i]

            slope = np.polyfit(x, y, 1)[0]
            slopes.append(slope)

        return np.mean(slopes)

    def _calc_anomaly_ratio(self, pred, history):

        mean = np.mean(history, axis=0)
        std = np.std(history, axis=0) + 1e-8

        z = np.abs((pred - mean) / std)

        return np.mean(z > 3)

    def _calc_jump(self, pred):
        return np.max(np.abs(np.diff(pred, axis=0)))

    def _calc_monotonic(self, pred):

        diff = np.diff(pred, axis=0)

        return max(np.sum(diff > 0), np.sum(diff < 0)) / (diff.size + 1e-8)

    def _calc_entropy(self, pred):

        hist, _ = np.histogram(pred.flatten(), bins=20)

        p = hist / np.sum(hist)
        p = p[p > 0]

        return -np.sum(p * np.log(p))

    def _calc_final_score(self, trend, anomaly_ratio, jump, monotonic, entropy):

        score = (
                100
                - anomaly_ratio * 50
                - jump * 2
                - monotonic * 20
                + trend * 30
                + entropy * 2
        )

        return max(0, min(100, score))

    def _evaluate(self, pred, history):

        volatility = self._calc_volatility(pred)
        smoothness = self._calc_smoothness(pred)
        trend = self._calc_trend(pred)
        anomaly_ratio = self._calc_anomaly_ratio(pred, history)
        jump = self._calc_jump(pred)
        monotonic = self._calc_monotonic(pred)
        entropy = self._calc_entropy(pred)

        final_score = self._calc_final_score(
            trend,
            anomaly_ratio,
            jump,
            monotonic,
            entropy
        )

        return {
            "final_score": final_score,
            "volatility": volatility,
            "smoothness": smoothness,
            "trend": trend,
            "anomaly_ratio": anomaly_ratio,
            "jump": jump,
            "monotonic": monotonic,
            "entropy": entropy
        }

    def predict_with_score(self, hours=1):

        print(f"预测未来 {hours}h")

        pred, raw, df = self._predict(hours)

        history = raw[-500:]

        scores = self._evaluate(pred, history)

        # 构建时间
        last_ts = df["timestamp"].iloc[-1]

        timestamps = [
            last_ts + pd.Timedelta(seconds=self.interval * (i + 1))
            for i in range(len(pred))
        ]

        result_df = pd.DataFrame(pred, columns=self.metrics)
        result_df["timestamp"] = timestamps

        score = scores["final_score"]
        trend = scores["trend"]
        volatility = scores["volatility"]
        anomaly_ratio = scores["anomaly_ratio"]
        evaluate = self.judge_status(score, trend, volatility, anomaly_ratio)

        return result_df, scores, evaluate

    def judge_status(self, score, trend, volatility, anomaly_ratio):

        if anomaly_ratio > 0.1:
            return "严重异常"

        if score < 30:
            return "高风险"

        if trend < -0.7:
            return "持续恶化"

        if volatility > 0.3:
            return "高波动"

        if score > 80:
            return "优秀"

        if score > 60:
            return "良好"

        return "一般"


# if __name__ == "__main__":
#
#     feature_columns = [
#         "cpu_usage", "response_time", "memory_usage",
#         "disk_usage", "io_read", "io_write",
#         "service_rt", "service_qps"
#     ]
#
#     predictor = MultiMetricPredictor(
#         r"D:\Python\pythonProject\ServicerAnomalySystem\data_generator\metrics.db",
#         "server_01_metrics"
#     )
#
#     future, scores, evaluate = predictor.predict_with_score()
#     print(future)
#
#     df = pd.DataFrame(future, columns=feature_columns)
#
#     # 时间戳生成
#     last_ts = predictor.reader.read_server_metrics(
#         predictor.table_name
#     )["timestamp"].iloc[-1]
#
#     df["timestamp"] = [
#         last_ts + (i + 1) * predictor.interval
#         for i in range(len(df))
#     ]
#
#     pd.set_option('display.max_rows', None)
#     pd.set_option('display.max_columns', None)
#     pd.set_option('display.width', None)
#
#     print("总体预测：")
#     print(evaluate)
#     print("\n评分：")
#     for k, v in scores.items():
#         print(f"{k}: {v:.4f}")
#     print(df)
