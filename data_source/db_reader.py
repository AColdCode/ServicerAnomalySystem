import datetime
import os
import sqlite3
import sys

import numpy as np
import pandas as pd


class DBReader:
    def __init__(self, db_path="data_generator/metrics.db"):
        self.db_path = db_path

    def _get_connection(self):
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller 打包后会创建临时文件夹
            base_path = sys._MEIPASS
        else:
            # 开发环境
            base_path = os.path.abspath(".")
        path = os.path.join(base_path, self.db_path)
        return sqlite3.connect(path, check_same_thread=False)

    def _get_table_columns(self, table_name):
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute(f"PRAGMA table_info({table_name})")
        columns = {row[1] for row in cur.fetchall()}
        conn.close()
        return columns

    def _resolve_real_anomaly_column(self, metric, columns):
        candidates = [f"{metric}_anomaly"]

        special_map = {
            "cpu_usage": "cpu_anomaly",
            "memory_usage": "memory_anomaly",
            "disk_usage": "disk_anomaly"
        }

        special_column = special_map.get(metric)
        if special_column:
            candidates.insert(0, special_column)

        for column in candidates:
            if column in columns:
                return column

        return None

    def get_server_tables(self):
        conn = self._get_connection()
        conn.execute("PRAGMA journal_mode=WAL;")

        query = """
        SELECT name FROM sqlite_master
        WHERE type='table'
        AND name LIKE 'server_%_metrics'
        """

        tables = pd.read_sql_query(query, conn)

        conn.close()

        return sorted(tables["name"].tolist())

    def get_latest_timestamp(self, table_name=None):
        conn = self._get_connection()
        cur = conn.cursor()

        if table_name:
            cur.execute(f"SELECT MAX(timestamp) FROM {table_name}")
            row = cur.fetchone()
            conn.close()
            return int(row[0]) if row and row[0] is not None else 0

        latest = 0
        for table in self.get_server_tables():
            cur.execute(f"SELECT MAX(timestamp) FROM {table}")
            row = cur.fetchone()
            if row and row[0] is not None:
                latest = max(latest, int(row[0]))

        conn.close()
        return latest

    def read_server_metrics(self, table_name):
        conn = self._get_connection()

        query = f"""
        SELECT *
        FROM {table_name}
        ORDER BY timestamp
        """

        df = pd.read_sql_query(query, conn)

        conn.close()

        return df

    def read_metrics_by_time(self, table_name, start_time, end_time):
        conn = self._get_connection()

        query = f"""
        SELECT *
        FROM {table_name}
        WHERE timestamp BETWEEN '{start_time}' AND '{end_time}'
        ORDER BY timestamp
        """

        df = pd.read_sql_query(query, conn)

        conn.close()

        return df

    def fetch_metric(self, table, metric, start_time, end_time):
        columns = self._get_table_columns(table)
        detect_column = f"{metric}_detect_anomaly"
        real_anomaly_column = self._resolve_real_anomaly_column(metric, columns)

        detect_expr = detect_column if detect_column in columns else "0"
        real_anomaly_expr = real_anomaly_column if real_anomaly_column else "0"

        conn = self._get_connection()
        cur = conn.cursor()

        query = f"""
        SELECT timestamp, {metric}, {detect_expr}, {real_anomaly_expr}
        FROM {table}
        WHERE timestamp BETWEEN ? AND ?
        ORDER BY timestamp ASC
        """

        cur.execute(query, (start_time, end_time))
        rows = cur.fetchall()
        conn.close()

        timestamps = []
        values = []
        detect_anomalies = []
        real_anomalies = []

        for ts, val, detect_flag, real_flag in rows:
            if val is not None:
                timestamps.append(ts)
                values.append(val)
                detect_anomalies.append(int(detect_flag) if detect_flag is not None else 0)
                real_anomalies.append(int(real_flag) if real_flag is not None else 0)

        return timestamps, values, detect_anomalies, real_anomalies

    def statistic_all_anomalies(self, metrics, start_time=None, end_time=None):
        """
        统计所有表、所有指标的异常情况

        :param metrics: 指标列表
        :param start_time: 可选
        :param end_time: 可选
        :return: dict
        """

        result = {}

        tables = self.get_server_tables()

        for table in tables:
            table_result = {}

            columns = self._get_table_columns(table)

            for metric in metrics:
                detect_col = f"{metric}_detect_anomaly"
                real_col = self._resolve_real_anomaly_column(metric, columns)

                # 不存在直接跳过
                if detect_col not in columns and not real_col:
                    continue

                detect_expr = detect_col if detect_col in columns else "0"
                real_expr = real_col if real_col else "0"

                # 时间过滤
                time_condition = ""
                params = []

                if start_time and end_time:
                    time_condition = "WHERE timestamp BETWEEN ? AND ?"
                    params = [start_time, end_time]

                query = f"""
                SELECT 
                    SUM({detect_expr}) as detect_count,
                    SUM({real_expr}) as real_count
                FROM {table}
                {time_condition}
                """

                conn = self._get_connection()
                cur = conn.cursor()
                cur.execute(query, params)
                row = cur.fetchone()
                conn.close()

                detect_count = row[0] if row[0] else 0
                real_count = row[1] if row[1] else 0

                table_result[metric] = {
                    "detect": detect_count,
                    "real": real_count
                }

            result[table] = table_result

        return result

    def statistic_total_anomalies(self, metrics, start_time=None, end_time=None):
        all_stats = self.statistic_all_anomalies(metrics, start_time, end_time)

        total = {}

        for table_data in all_stats.values():
            for metric, stat in table_data.items():
                if metric not in total:
                    total[metric] = {"detect": 0, "real": 0}

                total[metric]["detect"] += stat["detect"]
                total[metric]["real"] += stat["real"]

        return total

    def statistic_anomalies(self, metrics, start_time=None, end_time=None):
        all_stats = self.statistic_all_anomalies(metrics, start_time=None, end_time=None)
        all_anomalies = 0

        for table_data in all_stats.values():
            for metric, stat in table_data.items():
                all_anomalies += stat["detect"]
        return all_anomalies

    def read_multi_anomaly_results(self, table, metrics, start_time, end_time):
        """
        :param table:
        :param metrics:
        :param start_time:
        :param end_time:
        :return:
                {
                    "data": [
                        {
                            "time": "2026-04-18 12:30",
                            "score": 0.92,
                            "is_anomaly": 1,
                            "is_handled": 0,
                            "top_metric": "cpu_usage"
                            "timestamp": 1234567890
                        }
                    ],
                    "accuracy": 0.91,
                    "anomalyNum": 1
                }
        """
        conn = self._get_connection()
        cur = conn.cursor()

        # 检查字段是否存在（防止报错）
        columns = self._get_table_columns(table)

        contrib_cols = [f"{m}_contrib" for m in metrics if f"{m}_contrib" in columns]

        base_cols = [
            "timestamp",
            "multi_anomaly_score",
            "multi_detect_anomaly",
            "is_anomaly"
        ]

        # 可选字段
        if "is_handled" in columns:
            base_cols.append("is_handled")
        else:
            base_cols.append("0 as is_handled")

        select_cols = base_cols + contrib_cols

        query = f"""
        SELECT {",".join(select_cols)}
        FROM {table}
        WHERE timestamp BETWEEN ? AND ?
        ORDER BY timestamp ASC
        """

        cur.execute(query, (start_time, end_time))
        rows = cur.fetchall()
        conn.close()

        result = []

        correct = 0
        total = 0
        anomalyNum = 0

        for row in rows:
            ts = row[0]
            score = row[1]
            pred = row[2]
            real = row[3]
            handled = row[4]

            contrib_values = row[5:]

            # 时间转换
            dt = datetime.datetime.fromtimestamp(ts)
            time_str = dt.strftime("%Y-%m-%d %H:%M")

            # 最大贡献指标
            if contrib_values and sum(contrib_values) > 0:
                max_idx = int(np.argmax(contrib_values))
                top_metric = metrics[max_idx]
            else:
                top_metric = None

            result.append({
                "time": time_str,
                "score": float(score * 100) if score is not None else 0,
                "is_anomaly": int(pred),
                "is_handled": int(handled),
                "top_metric": top_metric,
                "timestamp": ts
            })

            # 准确率
            if real is not None:
                total += 1
                anomalyNum += int(pred)
                if int(pred) == int(real):
                    correct += 1

        accuracy = correct / total if total > 0 else 0

        return {
            "data": result,
            "accuracy": accuracy,
            "anomalyNum": anomalyNum
        }

    def readTimeAndMetric(self, table, metric, start_time, end_time):
        conn = self._get_connection()
        cur = conn.cursor()

        query = f"""
        SELECT timestamp, {metric}
        FROM {table}
        WHERE timestamp BETWEEN ? AND ?
        ORDER BY timestamp ASC
        """

        cur.execute(query, (start_time, end_time))
        rows = cur.fetchall()
        conn.close()

        timestamps = []
        values = []

        for ts, val in rows:
            if val is not None:
                timestamps.append(ts)
                values.append(val)

        return timestamps, values

    def readTimeAndMetrics(self, table, metrics, start_time, end_time):
        conn = self._get_connection()
        cur = conn.cursor()

        metrics_str = ', '.join(metrics)

        query = f"""
        SELECT timestamp, {metrics_str}
        FROM {table}
        WHERE timestamp BETWEEN ? AND ?
        ORDER BY timestamp ASC
        """

        cur.execute(query, (start_time, end_time))
        rows = cur.fetchall()
        conn.close()

        timestamps = []
        values_2d = [[] for _ in metrics]

        for row in rows:
            ts = row[0]
            metric_vals = row[1:]

            if all(v is None for v in metric_vals):
                continue

            timestamps.append(ts)
            for i, val in enumerate(metric_vals):
                values_2d[i].append(val)

        return timestamps, values_2d
