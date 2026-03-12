import numpy as np

from anomaly_detection.multi_metric.models.pca_model import PCAModel
from anomaly_detection.multi_metric.utils.metrics import PCAMetrics
from anomaly_detection.multi_metric.threshold.threshold_estimator import ThresholdEstimator


class PCADetector:
    """
    工业级 PCA 异常检测器

    主要功能：
    1 训练PCA模型
    2 计算异常统计量
    3 估计异常阈值
    4 执行异常检测
    """

    def __init__(self,
                 variance_ratio=0.9,
                 alpha=0.99,
                 robust_threshold=True):

        # PCA参数
        self.variance_ratio = variance_ratio

        # 阈值置信水平
        self.alpha = alpha

        # 是否使用稳健阈值
        self.robust_threshold = robust_threshold

        # 核心组件
        self.pca_model = PCAModel(variance_ratio=self.variance_ratio)

        self.metrics = None

        self.threshold = ThresholdEstimator(alpha=self.alpha)

        # 训练状态
        self.is_trained = False

    # =============================
    # 训练模型
    # =============================

    def fit(self, X):

        """
        使用训练数据建立PCA模型
        """

        # 训练PCA
        self.pca_model.fit(X)

        # 初始化指标计算器
        self.metrics = PCAMetrics(self.pca_model)

        # 计算训练统计量
        spe_scores, t2_scores = self.metrics.score(X)

        # 估计阈值
        if self.robust_threshold:

            self.threshold.fit_robust(
                spe_scores,
                t2_scores
            )

        else:

            self.threshold.fit(
                spe_scores,
                t2_scores
            )

        self.is_trained = True

    # =============================
    # 批量检测
    # =============================

    def detect(self, X):

        """
        对一批数据进行异常检测
        """

        if not self.is_trained:
            raise RuntimeError("Detector not trained")

        spe_scores, t2_scores = self.metrics.score(X)

        results = self.threshold.detect(
            spe_scores,
            t2_scores
        )

        return results, spe_scores, t2_scores

    # =============================
    # 单样本检测
    # =============================

    def detect_one(self, x):

        """
        检测单个样本
        """

        if not self.is_trained:
            raise RuntimeError("Detector not trained")

        spe, t2 = self.metrics.score_single(x)

        is_anomaly = self.threshold.is_anomaly(spe, t2)

        return is_anomaly, spe, t2

    # =============================
    # 获取阈值
    # =============================

    def get_thresholds(self):

        return self.threshold.get_thresholds()

    # =============================
    # 获取主成分数量
    # =============================

    def get_num_components(self):

        return self.pca_model.k

    # =============================
    # 获取模型
    # =============================

    def get_model(self):

        return self.pca_model
