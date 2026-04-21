"""
用于存储单指标异常检测的参数配置
"""


class DetectorConfig:
    """
    单指标异常检测配置类
    """

    # 滑动窗口大小
    WINDOW_SIZE = 288

    # 最小检测窗口
    MIN_WINDOW = 50

    # z-score 阈值
    ZSCORE_THRESHOLD = 5

    # 是否使用 EWMA 预测
    USE_EWMA = True

    # EWMA 平滑系数
    EWMA_ALPHA = 0.3

    # 是否使用 MAD 鲁棒检测
    USE_MAD = True

    # MAD 阈值
    MAD_THRESHOLD = 3.5
