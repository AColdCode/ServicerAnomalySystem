import sqlite3
import pandas as pd


class DBReader:
    def __init__(self, db_path="data_generator/metrics.db"):
        self.db_path = db_path

    def get_connection(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _get_table_columns(self, table_name):
        conn = self.get_connection()
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
        conn = self.get_connection()
        conn.execute("PRAGMA journal_mode=WAL;")

        query = """
        SELECT name FROM sqlite_master
        WHERE type='table'
        AND name LIKE 'server_%_metrics'
        """

        tables = pd.read_sql_query(query, conn)

        conn.close()

        return tables["name"].tolist()

    def read_server_metrics(self, table_name):
        conn = self.get_connection()

        query = f"""
        SELECT *
        FROM {table_name}
        ORDER BY timestamp
        """

        df = pd.read_sql_query(query, conn)

        conn.close()

        return df

    def read_metrics_by_time(self, table_name, start_time, end_time):
        conn = self.get_connection()

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

        conn = self.get_connection()
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

                conn = self.get_connection()
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
