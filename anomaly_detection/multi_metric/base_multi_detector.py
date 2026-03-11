import pandas as pd


class BaseMultiMetricDetector:
    """
    多指标异常检测父类
    """

    def __init__(self, metrics):

        self.metrics = metrics

    def detect(self, df: pd.DataFrame):

        raise NotImplementedError("子类必须实现 detect 方法")

    def export_to_csv(self, df, path):

        df.to_csv(path, index=False)

        print(f"检测结果保存至: {path}")

    def get_anomalies(self, df):

        return df[df["multi_anomaly"]]