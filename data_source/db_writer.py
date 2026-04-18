import sqlite3


class DBWriter:
    """
    数据库写入模块
    负责写入异常检测结果
    """

    def __init__(self, db_path="data_generator/metrics.db"):
        self.db_path = db_path

    def get_connection(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def ensure_column_exists(self, table, column_name, type="INTEGER"):

        conn = self.get_connection()
        conn.execute("PRAGMA journal_mode=WAL;")
        cursor = conn.cursor()

        cursor.execute(f"PRAGMA table_info({table})")
        columns = [col[1] for col in cursor.fetchall()]

        if column_name not in columns:
            cursor.execute(f"""
            ALTER TABLE {table}
            ADD COLUMN {column_name} {type} DEFAULT 0
            """)

        conn.commit()
        conn.close()

    def update_anomaly(self, table, timestamps, anomalies, column_name, type="INTEGER"):

        conn = self.get_connection()
        cursor = conn.cursor()

        if type == "INTEGER":
            # 批量更新（性能关键）
            cursor.executemany(f"""
            UPDATE {table}
            SET {column_name} = ?
            WHERE timestamp = ?
            """, [(int(a), int(ts)) for ts, a in zip(timestamps, anomalies)])
        elif type == "REAL":
            cursor.executemany(f"""
            UPDATE {table}
            SET {column_name} = ?
            WHERE timestamp = ?
            """, [(float(a), int(ts)) for ts, a in zip(timestamps, anomalies)])
        else:
            raise ValueError(f"Unsupported type: {type}")

        conn.commit()
        conn.close()

    def mark_anomaly_unhandled(self, table, timestamps, anomalies):
        """
        将检测为异常的数据标记为“未处理”（仅新增异常）
        """

        conn = self.get_connection()
        cursor = conn.cursor()

        # 确保列存在
        self.ensure_column_exists(table, "is_handled")

        # 只更新 anomaly = 1 的点
        update_data = [
            (0, int(ts))  # 0 = 未处理
            for ts, a in zip(timestamps, anomalies)
            if int(a) == 1
        ]

        cursor.executemany(f"""
        UPDATE {table}
        SET is_handled = ?
        WHERE timestamp = ?
        """, update_data)

        conn.commit()
        conn.close()

    def mark_anomaly_handled(self, table, timestamp):
        conn = self.get_connection()
        cursor = conn.cursor()

        # 确保列存在
        self.ensure_column_exists(table, "is_handled")

        cursor.execute(f"""
            UPDATE {table}
            SET is_handled = 1
            WHERE timestamp = ?
        """, (timestamp,))

        conn.commit()
        conn.close()
