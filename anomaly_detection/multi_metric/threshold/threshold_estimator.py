import numpy as np


class ThresholdEstimator:
    """
    PCA异常检测阈值估计器

    功能：
    1 计算SPE阈值
    2 计算T²阈值
    3 支持百分位数方法
    4 支持稳健阈值
    """

    def __init__(self, alpha=0.99):

        # 置信水平
        self.alpha = alpha

        # 阈值
        self.spe_threshold = None
        self.t2_threshold = None

    # ==================================
    # 基础分位数阈值
    # ==================================

    def percentile_threshold(self, scores):

        """
        使用分位数计算阈值
        """

        threshold = np.percentile(scores, self.alpha * 100)

        return threshold

    # ==================================
    # 稳健阈值 (去除极值)
    # ==================================

    def robust_threshold(self, scores):

        """
        使用 IQR 方法过滤极值
        """

        q1 = np.percentile(scores, 25)
        q3 = np.percentile(scores, 75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        filtered = scores[(scores >= lower) & (scores <= upper)]

        threshold = np.percentile(filtered, self.alpha * 100)

        return threshold

    # ==================================
    # 训练阈值
    # ==================================

    def fit(self, spe_scores, t2_scores):

        """
        根据训练数据计算阈值
        """

        self.spe_threshold = self.percentile_threshold(spe_scores)

        self.t2_threshold = self.percentile_threshold(t2_scores)

    # ==================================
    # 稳健训练
    # ==================================

    def fit_robust(self, spe_scores, t2_scores):

        """
        使用稳健方法训练阈值
        """

        self.spe_threshold = self.robust_threshold(spe_scores)

        self.t2_threshold = self.robust_threshold(t2_scores)

    # ==================================
    # 判断异常
    # ==================================

    def is_anomaly(self, spe, t2):

        """
        判断是否异常
        """

        if spe > self.spe_threshold:
            return True

        if t2 > self.t2_threshold:
            return True

        return False

    # ==================================
    # 批量判断
    # ==================================

    def detect(self, spe_scores, t2_scores):

        results = []

        for spe, t2 in zip(spe_scores, t2_scores):

            if self.is_anomaly(spe, t2):
                results.append(1)
            else:
                results.append(0)

        return np.array(results)

    # ==================================
    # 获取阈值
    # ==================================

    def get_thresholds(self):

        return self.spe_threshold, self.t2_threshold