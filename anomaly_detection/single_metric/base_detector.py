import numpy as np
from statsmodels.tsa.seasonal import STL


class BaseSingleMetricDetector:
    """
    单指标异常检测父类
    """

    def __init__(self, metric_name, period=288, z_threshold=3):
        self.metric = metric_name
        self.period = period
        self.z_threshold = z_threshold

    # ==========================
    # 异常检测主流程
    # ==========================
    def detect(self, df):
        series = df[self.metric]

        residual = self._stl_decompose(series)

        z_scores = self._zscore(residual)

        anomalies = np.abs(z_scores) > self.z_threshold

        df[f"{self.metric}_residual"] = residual
        df[f"{self.metric}_zscore"] = z_scores
        df[f"{self.metric}_anomaly"] = anomalies

        return df

    # ==========================
    # STL分解
    # ==========================
    def _stl_decompose(self, series):
        stl = STL(series, period=self.period)

        result = stl.fit()

        return result.resid

    # ==========================
    # ZScore
    # ==========================
    def _zscore(self, data):
        mean = np.mean(data)

        std = np.std(data)

        return (data - mean) / std

    # ==========================
    # 获取异常数据
    # ==========================
    def get_anomalies(self, df):
        return df[df[f"{self.metric}_anomaly"]]

    # =============================
    # 导出CSV
    # =============================
    def export_to_csv(self, df, output_path):
        df.to_csv(output_path, index=False)

        print(f"结果已保存到 {output_path}")
