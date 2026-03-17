import sqlite3
import pandas as pd
import numpy as np

from anomaly_detection.multi_metric.online.online_detector import OnlinePCADetector

DB_PATH = "../../../data_generator/metrics.db"
TABLE_NAME = "server_01_metrics"

OUT_CSV = "../../../results/server01/pca_detect.csv"


def load_data():
    """
    从数据库读取数据
    """

    conn = sqlite3.connect(DB_PATH)

    query = f"""
    SELECT *
    FROM {TABLE_NAME}
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def build_feature_matrix(df, metrics=None):
    if metrics is None:
        numeric_df = df.select_dtypes(include=["number"])
    else:
        numeric_df = df[metrics]

    numeric_df = numeric_df.fillna(0)

    # 删除常数列
    numeric_df = numeric_df.loc[:, numeric_df.std() > 1e-6]

    X = numeric_df.values

    return X, numeric_df.columns.tolist()


def run_detection(X):
    """
    运行在线检测
    """
    detector = OnlinePCADetector(
        window_size=288,
        variance_ratio=0.95,
        alpha=0.999,
    )

    results, spe_list, t2_list = detector.run(X)

    return results, spe_list, t2_list


def save_results(df, results, spe, t2):
    """
    保存检测结果
    """

    df["anomaly"] = results
    df["spe"] = spe
    df["t2"] = t2

    df.to_csv(OUT_CSV, index=False)

    print("Detection finished")
    print("Result saved to:", OUT_CSV)


def main():
    print("Loading data...")

    df = load_data()

    print("Rows:", len(df))

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

    X, feature_names = build_feature_matrix(df, metrics)

    print("Metrics:", feature_names)

    print("Running PCA anomaly detection...")

    results, spe, t2 = run_detection(X)

    save_results(df, results, spe, t2)


if __name__ == "__main__":
    main()
