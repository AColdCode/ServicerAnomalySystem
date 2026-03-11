import sqlite3
import pandas as pd


class DBReader:
    """
    SQLite数据库读取模块
    负责从 metrics.db 读取服务器监控数据
    """

    def __init__(self, db_path="../data_generator/metrics.db"):
        self.db_path = db_path

    def get_connection(self):
        """创建数据库连接"""
        return sqlite3.connect(self.db_path)

    def get_server_tables(self):
        """
        获取数据库中的服务器表
        返回:
            ['server_01_metrics', 'server_02_metrics', ...]
        """

        conn = self.get_connection()

        query = """
        SELECT name FROM sqlite_master
        WHERE type='table'
        AND name LIKE 'server_%_metrics'
        """

        tables = pd.read_sql_query(query, conn)

        conn.close()

        return tables["name"].tolist()

    def read_server_metrics(self, table_name):
        """
        读取某个服务器的全部监控数据
        """

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
        """
        按时间范围读取监控数据
        """

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
