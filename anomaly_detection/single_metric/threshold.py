from .config import DetectorConfig


class ThresholdJudge:
    """
    异常阈值判断模块
    """

    def __init__(self):

        self.z_threshold = DetectorConfig.ZSCORE_THRESHOLD

        self.mad_threshold = DetectorConfig.MAD_THRESHOLD

    # =============================
    # ZScore异常判断
    # =============================
    def is_zscore_anomaly(self, zscore):

        if abs(zscore) > self.z_threshold:
            return True

        return False

    # =============================
    # MAD异常判断
    # =============================
    def is_mad_anomaly(self, mad_score):

        if mad_score > self.mad_threshold:
            return True

        return False

    # =============================
    # 综合判断
    # =============================
    def judge(self, zscore, mad_score):

        """
        同时使用两种检测方法
        """

        z_flag = self.is_zscore_anomaly(zscore)

        mad_flag = self.is_mad_anomaly(mad_score)

        if z_flag or mad_flag:
            return 1

        return 0
