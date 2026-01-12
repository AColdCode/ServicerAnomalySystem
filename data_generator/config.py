# config.py
class Config:
    DB_NAME = "metrics.db"

    SERVER_COUNT = 10                # 服务器数量

    SAMPLE_INTERVAL_SEC = 300        # 数据采集周期 5 分钟
    DAYS = 180                       # 数据采集时间 6 个月
    POINTS_PER_DAY = 288
    TOTAL_POINTS = DAYS * POINTS_PER_DAY # 总数据点数

    DAY_PERIOD = POINTS_PER_DAY
    WEEK_PERIOD = POINTS_PER_DAY * 7

    # 异常参数
    ANOMALY_PROB = 0.002
    ANOMALY_MIN_LEN = 6              # 30 分钟
    ANOMALY_MAX_LEN = 18             # 90 分钟
