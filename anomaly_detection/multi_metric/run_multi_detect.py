from data_source.db_reader import DBReader
from preprocessing.preprocessor import TimeSeriesPreprocessor

from anomaly_detection.multi_metric.pca_mahalanobis_detector import PCAMahalanobisDetector


def main():
    reader = DBReader("../../data_generator/metrics.db")

    df = reader.read_server_metrics("server_01_metrics")

    # 预处理
    preprocessor = TimeSeriesPreprocessor()

    df = preprocessor.process(df)

    # 选择指标
    metrics = [
        "cpu_usage",
        "response_time",
        "memory_usage",
        "disk_usage",
        "io_read",
        "io_write",
        "service_rt",
        "service_qps"
    ]

    detector = PCAMahalanobisDetector(
        metrics=metrics,
        n_components=3,
        threshold=3.0
    )

    df = detector.detect(df)

    detector.export_to_csv(df, "../../results/server01_multi_detect.csv")

    anomalies = detector.get_anomalies(df)

    print("异常数量:", len(anomalies))


if __name__ == "__main__":
    main()
