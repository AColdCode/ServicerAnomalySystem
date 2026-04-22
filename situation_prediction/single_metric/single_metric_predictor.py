import torch
import numpy as np

from data_source.db_reader import DBReader
from preprocessing.preprocessor import TimeSeriesPreprocessor
from situation_prediction.single_metric.models.lstm_model import LSTMModel
from situation_prediction.single_metric.utils.model_manager import ModelManager
from situation_prediction.single_metric.scaler.scaler_manager import ScalerManager
from situation_prediction.single_metric.scaler.standard_scaler import StandardScaler


class SingleMetricPredictor:

    def __init__(self, metric, table_name, window_size=30,
                 db_path="data_generator/metrics.db"):

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

    # =========================
    # 预测
    # =========================
    def _predict(self, hours=1, interval_minutes=5):

        steps = int(hours * 60 / interval_minutes)

        model_name = f"{self.metric}_{steps}_model"
        model = LSTMModel(output_steps=steps)
        model = self.manager.load(model, self.table_name, model_name)

        model.to(self.device)
        model.eval()

        state = self.scaler_manager.load(self.table_name, self.metric)
        self.scaler.load_state_dict(state)

        df = self.reader.read_server_metrics(self.table_name)
        df = self.processor.process(df)

        values = df[self.metric].values

        diff = values[1:] - values[:-1]
        diff_norm = self.scaler.transform(diff)

        last_window = diff_norm[-self.window_size:]

        x = torch.tensor(last_window, dtype=torch.float32) \
            .unsqueeze(0).unsqueeze(-1).to(self.device)

        with torch.no_grad():
            pred_diff_norm = model(x).cpu().numpy().flatten()

        pred_diff = self.scaler.inverse_transform(pred_diff_norm)
        pred_diff = np.clip(pred_diff, -5, 5)

        last_val = values[-1]

        future = []
        cur = last_val

        for d in pred_diff:
            cur += d
            future.append(cur)

        return np.array(future), values

    # =========================
    # 风险建模（核心）
    # =========================
    def _calc_risk_series(self, pred, history):

        pred = np.array(pred)

        # 1. 局部突变风险（核心）
        diff_risk = np.abs(np.diff(pred))
        diff_risk = np.insert(diff_risk, 0, 0)

        # 2. 偏离历史分布风险
        mean = np.mean(history)
        std = np.std(history) + 1e-8
        z_risk = np.abs((pred - mean) / std)

        # 3. 融合风险
        risk = 0.6 * diff_risk + 0.4 * z_risk

        return risk

    def _calc_risk_metrics(self, risk):

        return {
            "risk_intensity": float(np.mean(risk)),
            "risk_peak": float(np.max(risk)),
            "risk_ratio": float(np.mean(risk > np.percentile(risk, 90)))
        }

    # =========================
    # 风险状态判定
    # =========================
    def judge_status(self, risk_metrics, score):

        risk = risk_metrics["risk_intensity"]

        if risk > 2.5:
            return "严重异常风险"

        if risk > 1.8:
            return "高风险"

        if risk > 1.2:
            return "中风险"

        if score > 80:
            return "稳定"

        return "低风险"

    # 对外接口
    def predict_with_score(self, hours=1, interval_minutes=5):

        print(f"预测 {self.metric} 未来 {hours}h")

        pred, history = self._predict(hours, interval_minutes)

        history = history[-500:]

        risk_series = self._calc_risk_series(pred, history)
        risk_metrics = self._calc_risk_metrics(risk_series)

        score = 100 * np.exp(-risk_metrics["risk_intensity"] / 2.0)

        status = self.judge_status(risk_metrics, score)

        return pred, {
            "final_score": float(score),

            "risk_intensity": risk_metrics["risk_intensity"],
            "risk_peak": risk_metrics["risk_peak"],
            "risk_ratio": risk_metrics["risk_ratio"],

            "risk_series": risk_series.tolist()
        }, status


# =========================
# test
# =========================
if __name__ == "__main__":

    predictor = SingleMetricPredictor(
        "io_write",
        "server_01_metrics",
        30,
        r"D:\Python\pythonProject\ServicerAnomalySystem\data_generator\metrics.db"
    )

    data, scores, status = predictor.predict_with_score(1)

    print(scores)
    print(status)
    print(data)
