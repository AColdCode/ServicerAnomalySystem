import pandas as pd

from data_source.db_reader import DBReader
from data_source.db_writer import DBWriter
from preprocessing.preprocessor import TimeSeriesPreprocessor
from anomaly_detection.single_metric.detector import SingleMetricDetector


class SingleMetricDetectionService:
    """
    单指标异常检测服务类
    """

    def __init__(self, db_path, table_name, metric):

        self.db_path = db_path
        self.table_name = table_name
        self.metric = metric

        self.reader = DBReader(db_path)
        self.writer = DBWriter(db_path)
        self.processor = TimeSeriesPreprocessor()
        self.detector = SingleMetricDetector()

        self.df = None
        self.results = None

    # 读取数据
    def load_data(self):
        self.df = self.reader.read_server_metrics(self.table_name)

    # 预处理
    def preprocess(self):
        self.df = self.processor.process(self.df)

    # 异常检测
    def detect(self):

        timestamps = (self.df["timestamp"].astype("int64") // 10 ** 9).tolist()
        values = self.df[self.metric].tolist()

        self.results = self.detector.detect(timestamps, values)

    # 写入数据库
    def save_to_db(self):

        result_df = pd.DataFrame(self.results)

        timestamps = result_df["timestamp"].tolist()
        anomalies = result_df["anomaly"].tolist()

        column_name = f"{self.metric}_detect_anomaly"

        # 1. 确保列存在
        self.writer.ensure_column_exists(self.table_name, column_name)

        # 2. 写入数据
        self.writer.update_anomaly(
            self.table_name,
            timestamps,
            anomalies,
            column_name
        )

    # 总流程
    def run(self):
        self.load_data()
        self.preprocess()
        self.detect()
        self.save_to_db()
