import pandas as pd
import numpy as np


class TimeSeriesPreprocessor:
    """
    时间序列数据预处理模块
    """

    def __init__(self):
        pass

    # =============================
    # 主预处理流程
    # =============================
    def process(self, df):

        df = self._format_timestamp(df)

        # df = self._sort_by_time(df)

        df = self._handle_missing_values(df)

        # df = self._remove_outliers(df)

        # df = self._generate_time_features(df)

        return df

    # =============================
    # 时间格式处理
    # =============================
    def _format_timestamp(self, df):

        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

        return df

    # =============================
    # 按时间排序
    # =============================
    def _sort_by_time(self, df):

        df = df.sort_values("timestamp")

        df = df.reset_index(drop=True)

        return df

    # =============================
    # 缺失值处理
    # =============================
    def _handle_missing_values(self, df):

        # 前向填充
        df.ffill(inplace=True)

        # 后向填充
        df.bfill(inplace=True)

        return df

    # =============================
    # 异常值过滤
    # =============================
    def _remove_outliers(self, df):

        numeric_cols = df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)

            Q3 = df[col].quantile(0.75)

            IQR = Q3 - Q1

            lower = Q1 - 1.5 * IQR

            upper = Q3 + 1.5 * IQR

            df[col] = df[col].clip(lower, upper)

        return df

    # =============================
    # 时间特征生成
    # =============================
    def _generate_time_features(self, df):

        df["hour"] = df["timestamp"].dt.hour

        df["day_of_week"] = df["timestamp"].dt.dayofweek

        df["day"] = df["timestamp"].dt.day

        df["month"] = df["timestamp"].dt.month

        return df

    # =============================
    # 数据标准化
    # =============================
    def normalize(self, df, columns):

        for col in columns:

            min_val = df[col].min()

            max_val = df[col].max()

            if max_val - min_val != 0:
                df[col] = (df[col] - min_val) / (max_val - min_val)

        return df
