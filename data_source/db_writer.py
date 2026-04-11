import sqlite3


class DBWriter:
    """
    数据库写入模块
    负责写入异常检测结果
    """

    def __init__(self, db_path):
        self.db_path = db_path

    def get_connection(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def ensure_column_exists(self, table, column_name):

        conn = self.get_connection()
        conn.execute("PRAGMA journal_mode=WAL;")
        cursor = conn.cursor()

        cursor.execute(f"PRAGMA table_info({table})")
        columns = [col[1] for col in cursor.fetchall()]

        if column_name not in columns:
            cursor.execute(f"""
            ALTER TABLE {table}
            ADD COLUMN {column_name} INTEGER DEFAULT 0
            """)

        conn.commit()
        conn.close()

    def update_anomaly(self, table, timestamps, anomalies, column_name):

        conn = self.get_connection()
        cursor = conn.cursor()

        # 批量更新（性能关键）
        cursor.executemany(f"""
        UPDATE {table}
        SET {column_name} = ?
        WHERE timestamp = ?
        """, [(int(a), int(ts)) for ts, a in zip(timestamps, anomalies)])

        conn.commit()
        conn.close()
