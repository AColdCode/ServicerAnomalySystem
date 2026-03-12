import numpy as np
from collections import deque

from anomaly_detection.multi_metric.detector.pca_detector import PCADetector


class OnlinePCADetector:
    """
    在线PCA异常检测器

    功能：
    1 滑动窗口训练
    2 实时异常检测
    3 自动更新窗口
    """

    def __init__(self,
                 window_size=288,
                 variance_ratio=0.9,
                 alpha=0.999,
                 robust_threshold=True):

        # 滑动窗口大小
        self.window_size = window_size

        # 数据窗口
        self.window = deque(maxlen=window_size)

        # PCA检测器
        self.detector = PCADetector(
            variance_ratio=variance_ratio,
            alpha=alpha,
            robust_threshold=robust_threshold
        )

        # 是否已训练
        self.is_trained = False

        # 异常计数
        self.anomaly_count = 0

    # =============================
    # 初始化窗口
    # =============================

    def init_window(self, X):

        """
        使用历史数据初始化窗口
        """

        for x in X:
            self.window.append(x)

        if len(self.window) == self.window_size:

            window_data = np.array(self.window)

            self.detector.fit(window_data)

            self.is_trained = True

    # =============================
    # 添加数据
    # =============================

    def process(self, x):

        """
        处理新数据点
        """

        x = np.array(x)

        # 如果还没训练
        if not self.is_trained:

            self.window.append(x)

            if len(self.window) == self.window_size:

                window_data = np.array(self.window)

                self.detector.fit(window_data)

                self.is_trained = True

            return False, None, None

        # 检测异常
        is_anomaly, spe, t2 = self.detector.detect_one(x)

        # 更新窗口
        self.window.append(x)

        return is_anomaly, spe, t2

    # =============================
    # 批量处理
    # =============================

    def run(self, X):

        """
        处理整个时间序列
        """

        results = []
        spe_list = []
        t2_list = []

        for x in X:

            is_anomaly, spe, t2 = self.process(x)

            results.append(is_anomaly)

            spe_list.append(spe)
            t2_list.append(t2)

        return results, spe_list, t2_list

    # =============================
    # 获取窗口数据
    # =============================

    def get_window(self):

        return np.array(self.window)

    # =============================
    # 获取阈值
    # =============================

    def get_thresholds(self):

        return self.detector.get_thresholds()