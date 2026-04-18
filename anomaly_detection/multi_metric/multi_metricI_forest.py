from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy as np

from data_source.db_reader import DBReader
from data_source.db_writer import DBWriter


class MultiMetricIForest:
    def __init__(self, db_path, table_name, metrics):
        self.db_path = db_path
        self.table_name = table_name

        self.reader = DBReader(db_path)
        self.writer = DBWriter(db_path)
        self.metrics = metrics

        self.model = None
        self.scaler = StandardScaler()

        # 用于贡献计算
        self.mean = None
        self.std = None

    # =========================
    # 数据构建
    # =========================
    def _build_feature_matrix(self, df):
        df = df[["timestamp"] + self.metrics].dropna()

        timestamps = df["timestamp"].tolist()
        X = df[self.metrics].values

        return timestamps, X

    # =========================
    # 训练模型
    # =========================
    def _fit(self, X):
        split = int(len(X) * 0.7)

        X_train = X[:split]

        X_scaled = self.scaler.fit_transform(X_train)

        self.model = IsolationForest(
            n_estimators=200,
            contamination=0.1,
            random_state=42
        )
        self.model.fit(X_scaled)

        # 用“正常数据”统计
        self.mean = np.mean(X_train, axis=0)
        self.std = np.std(X_train, axis=0) + 1e-8

        return self.scaler.transform(X)  # 返回全量

    # =========================
    # 异常检测
    # =========================
    def _predict(self, X_scaled):
        preds = self.model.predict(X_scaled)
        anomalies = np.where(preds == -1, 1, 0)

        raw_scores = self.model.score_samples(X_scaled)

        # 用 percentile 做归一化
        min_s = np.percentile(raw_scores, 5)
        max_s = np.percentile(raw_scores, 95)

        scores = (max_s - raw_scores) / (max_s - min_s + 1e-8)

        # clip到0~1
        scores = np.clip(scores, 0, 1)

        return anomalies.tolist(), scores.tolist()

    # =========================
    # 异常贡献计算
    # =========================
    def _compute_contributions(self, X, anomalies):
        contributions = []

        for x, is_anomaly in zip(X, anomalies):

            if is_anomaly == 0:
                contributions.append([0] * len(self.metrics))
                continue

            deviation = np.abs((x - self.mean) / self.std)

            total = np.sum(deviation) + 1e-8
            contrib = deviation / total

            contributions.append(contrib.tolist())

        return contributions

    # =========================
    # 单表处理
    # =========================
    def process_table(self):
        print(f"处理表: {self.table_name}")

        df = self.reader.read_server_metrics(self.table_name)

        timestamps, X = self._build_feature_matrix(df)
        X = self.add_diff_feature(X)

        if len(X) < 50:
            print("数据不足，跳过")
            return

        X_scaled = self._fit(X)

        anomalies, scores = self._predict(X_scaled)

        contributions = self._compute_contributions(X, anomalies)

        # =========================
        # 写入数据库
        # =========================
        anomaly_col = "multi_detect_anomaly"
        score_col = "multi_anomaly_score"

        self.writer.ensure_column_exists(self.table_name, anomaly_col)
        self.writer.ensure_column_exists(self.table_name, score_col, "REAL")

        # 每个指标的贡献列
        contrib_cols = [f"{m}_contrib" for m in self.metrics]
        for col in contrib_cols:
            self.writer.ensure_column_exists(self.table_name, col, "REAL")

        # 写 anomaly
        self.writer.update_anomaly(self.table_name, timestamps, anomalies, anomaly_col)

        # 标记未处理
        self.writer.mark_anomaly_unhandled(self.table_name, timestamps, anomalies)

        # 写 score
        self.writer.update_anomaly(self.table_name, timestamps, scores, score_col, "REAL")

        # 写 contribution（逐列）
        for i, metric in enumerate(self.metrics):
            col = f"{metric}_contrib"
            values = [c[i] for c in contributions]

            self.writer.update_anomaly(self.table_name, timestamps, values, col, "REAL")

    def add_diff_feature(self, X):
        diff = np.diff(X, axis=0)
        diff = np.vstack([diff[0], diff])  # 对齐

        return np.hstack([X, diff])

    # =========================
    # 全部表处理
    # =========================
    def run(self):
        self.process_table()
