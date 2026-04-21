"""
时间序列预测器
"""

from .config import DetectorConfig


class Predictor:
    """
    单指标预测器
    """

    def __init__(self):

        self.last_prediction = None

    def predict(self, history):

        if len(history) == 0:
            return 0

        return history[-1]

    def _mean_predict(self, history):
        """
        均值预测
        """

        return sum(history) / len(history)

    def _ewma_predict(self, history):
        """
        EWMA预测
        """

        alpha = DetectorConfig.EWMA_ALPHA

        ewma = history[0]

        for value in history[1:]:
            ewma = alpha * value + (1 - alpha) * ewma

        return ewma
