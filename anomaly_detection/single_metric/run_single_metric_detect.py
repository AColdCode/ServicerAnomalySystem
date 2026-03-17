import pandas as pd

from data_source.db_reader import DBReader
from preprocessing.preprocessor import TimeSeriesPreprocessor

from anomaly_detection.single_metric.detector import SingleMetricDetector


DB_PATH = "../../data_generator/metrics.db"

TABLE_NAME = "server_01_metrics"

METRIC = "cpu_usage"

OUT_CSV = "../../results/server01/"

ANOMALY_COLUMN_MAP = {
    "cpu_usage": "cpu_anomaly",
    "response_time": "response_time_anomaly",
    "memory_usage": "memory_anomaly",
    "disk_usage": "disk_anomaly",
    "io_read": "io_read_anomaly",
    "io_write": "io_write_anomaly",
    "service_rt": "service_rt_anomaly",
    "service_qps": "service_qps_anomaly"
}


def main():

    # =============================
    # 读取数据库
    # =============================
    reader = DBReader(DB_PATH)

    df = reader.read_server_metrics(TABLE_NAME)

    # =============================
    # 数据预处理
    # =============================
    processor = TimeSeriesPreprocessor()

    df = processor.process(df)

    # =============================
    # 获取指标
    # =============================
    timestamps = df["timestamp"].tolist()

    values = df[METRIC].tolist()

    # =============================
    # 异常检测
    # =============================
    detector = SingleMetricDetector()

    results = detector.detect(
        timestamps,
        values
    )

    # =============================
    # 保存结果
    # =============================
    result_df = pd.DataFrame(results)

    # 获取真实异常列
    real_anomaly_col = ANOMALY_COLUMN_MAP[METRIC]

    # 添加真实异常标签
    result_df[METRIC] = df[METRIC].values
    result_df[real_anomaly_col] = df[real_anomaly_col].values

    # 算法检测异常
    result_df["detect_anomaly"] = result_df["anomaly"]

    # 只保留需要列
    result_df = result_df[
        [
            "timestamp",
            METRIC,
            real_anomaly_col,
            "detect_anomaly"
        ]
    ]

    outPath = OUT_CSV + METRIC + "_detect.csv"
    result_df.to_csv(outPath, index=False)

    print("检测完成")
    print("结果保存:", outPath)


if __name__ == "__main__":
    main()
