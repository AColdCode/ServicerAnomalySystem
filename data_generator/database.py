# database.py
# | 字段名           | 含义        | 说明                  |
# | ------------- | --------- | ------------------- |
# | timestamp     | 时间戳       | Unix 时间戳（秒）         |
# | cpu_usage     | CPU 使用率   | 极低、平滑               |
# | response_time | 请求响应时间（秒） | 系统级                 |
# | memory_usage  | 内存使用率     | 百分比                 |
# | disk_usage    | 磁盘使用率     | 百分比                 |
# | io_read       | 磁盘读速率     | MB/s（模拟）            |
# | io_write      | 磁盘写速率     | MB/s（模拟）            |
# | service_rt    | 微服务响应时间   | 通常略高于 response_time |
# | service_qps   | 微服务吞吐量    | 与 RT 负相关            |
# | is_anomaly    | 是否异常      | 0 / 1               |

import sqlite3


class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_server_table(self, server_id):
        table = f"server_{server_id:02d}_metrics"
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,

            cpu_usage REAL,
            response_time REAL,
            memory_usage REAL,
            disk_usage REAL,
            io_read REAL,
            io_write REAL,
            service_rt REAL,
            service_qps REAL,

            is_anomaly INTEGER
        )
        """)
        self.conn.commit()

    def insert(self, table, record):
        placeholders = ",".join(["?"] * len(record))
        self.cursor.execute(
            f"INSERT INTO {table} VALUES (NULL,{placeholders})",
            record
        )

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
