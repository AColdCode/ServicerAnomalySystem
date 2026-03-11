import numpy as np
import pandas as pd

from anomaly_detection.multi_metric.base_multi_detector import BaseMultiMetricDetector
from anomaly_detection.multi_metric.scaler import StandardScaler
from anomaly_detection.multi_metric.pca_model import PCA
from anomaly_detection.multi_metric.mahalanobis import MahalanobisDistance


class PCAMahalanobisDetector(BaseMultiMetricDetector):
    """
    PCA + Mahalanobis 多指标异常检测
    """

    def __init__(self, metrics, n_components=2, threshold=3.0):

        super().__init__(metrics)

        self.n_components = n_components

        self.threshold = threshold

        self.scaler = StandardScaler()

        self.pca = PCA(n_components)

        self.md = MahalanobisDistance()

    def detect(self, df: pd.DataFrame):

        X = df[self.metrics].values

        # 标准化
        X_scaled = self.scaler.fit_transform(X)

        # PCA降维
        X_pca = self.pca.fit_transform(X_scaled)

        # Mahalanobis训练
        self.md.fit(X_pca)

        distances = self.md.batch_distance(X_pca)

        df["multi_distance"] = distances

        df["multi_anomaly"] = distances > self.threshold

        # 保存降维结果
        for i in range(self.n_components):

            df[f"pca_{i+1}"] = X_pca[:, i]

        return df