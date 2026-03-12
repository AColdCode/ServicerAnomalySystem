from .config import DetectorConfig
from .sliding_window import SlidingWindow
from .predictor import Predictor
from .residual_analyzer import ResidualAnalyzer
from .threshold import ThresholdJudge


class SingleMetricDetector:
    """
    单指标异常检测核心模块
    """

    def __init__(self):

        # 配置
        self.window_size = DetectorConfig.WINDOW_SIZE

        # 滑动窗口
        self.window = SlidingWindow(self.window_size)

        # 预测器
        self.predictor = Predictor()

        # 残差分析
        self.residual_analyzer = ResidualAnalyzer()

        # 阈值判断
        self.threshold = ThresholdJudge()

        # 检测结果
        self.results = []

    # =============================
    # 主检测流程
    # =============================
    def detect(self, timestamps, values):

        for i in range(len(values)):

            value = values[i]
            timestamp = timestamps[i]

            # 获取历史窗口
            history = self.window.values()

            # 如果窗口为空
            if len(history) == 0:
                predict = value
                residual = 0
                zscore = 0
                mad_score = 0
                anomaly = 0

            else:

                predict = self.predictor.predict(history)

                residual = self.residual_analyzer.compute_residual(
                    value, predict
                )

                zscore = self.residual_analyzer.compute_zscore(
                    residual
                )

                mad_score = self.residual_analyzer.compute_mad_score(
                    residual
                )

                anomaly = self.threshold.judge(
                    zscore,
                    mad_score
                )

            # 保存结果
            self.results.append({
                "timestamp": timestamp,
                "predict": predict,
                "residual": residual,
                "zscore": zscore,
                "mad_score": mad_score,
                "anomaly": anomaly
            })

            # 更新窗口(异常数据不更新窗口)
            if anomaly == 0:
                self.window.append(value)

        return self.results
