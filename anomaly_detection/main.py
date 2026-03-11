from data_source.db_reader import DBReader
from preprocessing.preprocessor import TimeSeriesPreprocessor
from anomaly_detection.single_metric.cpu_detector import CpuAnomalyDetector


def main():
    reader = DBReader("../data_generator/metrics.db")

    df = reader.read_server_metrics("server_01_metrics")

    # 预处理
    preprocessor = TimeSeriesPreprocessor()
    df = preprocessor.process(df)

    # CPU异常检测
    detector = CpuAnomalyDetector()

    df = detector.detect(df)

    # 保存CSV
    detector.export_to_csv(df, "../results/server01_cpu_detect.csv")


if __name__ == "__main__":
    main()
