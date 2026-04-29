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

    # 时间特征
    def _add_time_features(self, df):
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        hour = df["timestamp"].dt.hour
        df["sin_hour"] = np.sin(2 * np.pi * hour / 24)
        df["cos_hour"] = np.cos(2 * np.pi * hour / 24)
        return df

    # 构建输入
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

    # 模型加载
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

    # 预测
    def _predict(self, hours):

        steps = int(hours * 3600 / self.interval)

        model = self._load_model(steps)
        self._load_scaler()

        df = self.reader.read_server_metrics(self.table_name)

        data_norm, raw, df = self._build_input(df)

        last_window = data_norm[-self.window_size:]

        x = torch.tensor(last_window, dtype=torch.float32) \
            .unsqueeze(0).to(self.device)

        with torch.no_grad():
            pred_norm = model(x).cpu().numpy()[0]

        tmp = np.zeros((pred_norm.shape[0], self.scaler.mean.shape[0]))
        tmp[:, :8] = pred_norm

        pred = self.scaler.inverse_transform(tmp)[:, :8]
        pred = np.clip(pred, 0, None)

        return pred, raw, df

    # 风险建模
    def _calc_risk_series(self, pred, history):

        pred = np.array(pred)

        # 单指标风险
        diff = np.abs(np.diff(pred, axis=0))
        diff = np.vstack([np.zeros((1, pred.shape[1])), diff])

        mean = np.mean(history, axis=0)
        std = np.std(history, axis=0) + 1e-8

        z = np.abs((pred - mean) / std)

        risk_each = 0.6 * diff + 0.4 * z

        # 系统级风险
        risk_mean = np.mean(risk_each, axis=1)
        risk_std = np.std(risk_each, axis=1)

        risk_system = 0.7 * risk_mean + 0.3 * risk_std

        return risk_each, risk_system

    # 相关性变化（关键）
    def _calc_correlation_change(self, pred, history):

        hist_corr = np.corrcoef(history.T)
        pred_corr = np.corrcoef(pred.T)

        diff = np.abs(hist_corr - pred_corr)

        return float(np.mean(diff))

    # 评估
    def _evaluate(self, pred, history):

        risk_each, risk_system = self._calc_risk_series(pred, history)

        if len(pred) < 30:
            corr_change = 0.0
        else:
            corr_change = self._calc_correlation_change(pred, history)
            corr_change = min(corr_change, 0.3)

        risk_intensity = float(np.mean(risk_system))
        risk_peak = float(np.max(risk_system))
        risk_ratio = float(np.mean(risk_system > np.percentile(risk_system, 90)))

        score = (
                70 * np.exp(-risk_intensity)
                + 30 * (1 - corr_change)
        )

        return {
            "final_score": float(score),

            "risk_intensity": risk_intensity,
            "risk_peak": risk_peak,
            "risk_ratio": risk_ratio,

            "correlation_change": corr_change
        }

    # 状态判断
    def judge_status(self, scores):

        r = scores["risk_intensity"]
        corr = scores["correlation_change"]

        if r > 2.5:
            return "系统级异常风险"

        if r > 1.8:
            return "高风险"

        if corr > 0.5 and r > 1.0:
            return "结构异常"

        if r > 1.2:
            return "中风险"

        if scores["final_score"] > 80:
            return "稳定"

        return "低风险"

    # 对外接口
    def predict_with_score(self, hours=1):
        pred, raw, df = self._predict(hours)

        history = raw[-500:]

        scores = self._evaluate(pred, history)
        status = self.judge_status(scores)

        # 时间戳构建
        last_ts = df["timestamp"].iloc[-1]

        timestamps = [
            last_ts + pd.Timedelta(seconds=self.interval * (i + 1))
            for i in range(len(pred))
        ]

        result_df = pd.DataFrame(pred, columns=self.metrics)
        result_df["timestamp"] = timestamps

        return result_df, scores, status


# 测试
if __name__ == "__main__":

    predictor = MultiMetricPredictor(
        r"D:\Python\pythonProject\ServicerAnomalySystem\data_generator\metrics.db",
        "server_02_metrics"
    )

    future, scores, status = predictor.predict_with_score(6)

    print(future)
    print("\n评分：")
    for k, v in scores.items():
        if isinstance(v, float):
            print(f"{k}: {v:.4f}")

    print("\n状态：", status)
