import sqlite3
import random
import math
from datetime import datetime, timedelta


class MetricsGenerator:

    def __init__(self, db_name="metrics.db"):
        self.db_name = db_name

    # -----------------------------
    # 时间解析
    # -----------------------------
    def _parse_time(self, time_str):
        return datetime.strptime(time_str, "%Y/%m/%d %H:%M")

    # -----------------------------
    # 周期函数
    # -----------------------------
    def _day_cycle(self, t):
        seconds = t.hour * 3600 + t.minute * 60
        return math.sin(2 * math.pi * seconds / 86400)

    def _week_cycle(self, t):
        return math.sin(2 * math.pi * t.weekday() / 7)

    def _noise(self, scale):
        return random.uniform(-scale, scale)

    # -----------------------------
    # 业务负载
    # -----------------------------
    def _generate_load(self, t, capacity):
        base = 60 * capacity
        daily = 25 * self._day_cycle(t)
        weekly = 12 * self._week_cycle(t)

        load = base + daily + weekly + self._noise(4)
        return max(load, 5)

    # -----------------------------
    # 指标生成
    # -----------------------------
    def _generate_metrics(self, load, capacity):
        qps = load

        cpu = 0.004 + load * 0.00009 / capacity + self._noise(0.001)
        rt = 0.05 + load * 0.0012 + self._noise(0.01)
        srt = rt * (1 + self._noise(0.05))

        mem = 3 + load * 0.06 + self._noise(0.5)
        read = 30 + load * 0.9 + self._noise(5)
        write = 20 + load * 0.6 + self._noise(4)

        disk = 10 + (read + write) * 0.01 + self._noise(0.4)

        return cpu, rt, mem, disk, read, write, srt, qps

    # -----------------------------
    # 异常传播
    # -----------------------------
    def _propagate(self, cpu, rt, mem, disk, read, write, srt, qps, amp, anomaly_type):

        flags = [0] * 8

        if anomaly_type == "cpu":
            cpu *= amp * 4
            rt *= amp
            qps *= 0.7
            flags[0] = flags[1] = 1

        elif anomaly_type == "response":
            rt *= amp * 5
            srt = rt
            qps *= 0.6
            flags[1] = flags[6] = 1

        elif anomaly_type == "memory":
            mem *= amp * 3
            flags[2] = 1

        elif anomaly_type == "disk":
            disk *= amp * 3
            flags[3] = 1

        elif anomaly_type == "io_read":
            read *= amp * 5
            disk *= amp
            flags[4] = flags[3] = 1

        elif anomaly_type == "io_write":
            write *= amp * 5
            disk *= amp
            flags[5] = flags[3] = 1

        elif anomaly_type == "service_rt":
            srt *= amp * 5
            rt = srt
            qps *= 0.5
            flags[6] = flags[1] = 1

        elif anomaly_type == "qps":
            qps *= amp * 3
            cpu *= amp
            rt *= amp
            flags[7] = flags[0] = flags[1] = 1

        return (cpu, rt, mem, disk, read, write, srt, qps, *flags)

    # -----------------------------
    # 建表
    # -----------------------------
    def _create_table(self, cur, table):
        cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER UNIQUE,

            cpu_usage REAL,
            response_time REAL,
            memory_usage REAL,
            disk_usage REAL,
            io_read REAL,
            io_write REAL,
            service_rt REAL,
            service_qps REAL,

            is_anomaly INTEGER,

            cpu_anomaly INTEGER,
            response_time_anomaly INTEGER,
            memory_anomaly INTEGER,
            disk_anomaly INTEGER,
            io_read_anomaly INTEGER,
            io_write_anomaly INTEGER,
            service_rt_anomaly INTEGER,
            service_qps_anomaly INTEGER,

            root_cause TEXT
        )
        """)

    # -----------------------------
    # 单服务器生成
    # -----------------------------
    def _generate_server(self, cur, table, capacity, start, end, interval, anomaly_ratio):

        t = start

        anomaly_left = 0
        anomaly_len = 0
        anomaly_type = None
        cooldown = 0

        memory_leak = False
        leak_step = 0

        while t < end:

            load = self._generate_load(t, capacity)
            cpu, rt, mem, disk, read, write, srt, qps = self._generate_metrics(load, capacity)

            flags = [0] * 8
            root_cause = "normal"

            # 触发异常
            if anomaly_left == 0 and cooldown == 0:
                if random.random() < anomaly_ratio:
                    anomaly_type = random.choice([
                        "cpu", "response", "memory",
                        "disk", "io_read", "io_write",
                        "service_rt", "qps"
                    ])
                    anomaly_len = random.randint(3, 12)
                    anomaly_left = anomaly_len

            # 执行异常
            if anomaly_left > 0:
                step = anomaly_len - anomaly_left + 1
                amp = 1 + 3 * math.sin(math.pi * step / anomaly_len)

                result = self._propagate(
                    cpu, rt, mem, disk, read, write, srt, qps,
                    amp, anomaly_type
                )

                cpu, rt, mem, disk, read, write, srt, qps = result[:8]
                flags = list(result[8:])

                root_cause = anomaly_type
                anomaly_left -= 1

                if anomaly_left == 0:
                    cooldown = random.randint(12, 36)

            if cooldown > 0:
                cooldown -= 1

            # memory leak
            if not memory_leak and random.random() < 0.0004:
                memory_leak = True
                leak_step = 0

            if memory_leak:
                mem += leak_step * 0.2
                flags[2] = 1
                root_cause = "memory_leak"
                leak_step += 1

                if leak_step > random.randint(24, 48):
                    memory_leak = False

            is_anomaly = int(any(flags))

            cur.execute(
                f"""
                INSERT INTO {table} VALUES (
                NULL,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,
                ?)
                """,
                (
                    int(t.timestamp()),
                    cpu, rt, mem, disk, read, write, srt, qps,
                    is_anomaly,
                    *flags,
                    root_cause
                )
            )

            t += interval

    def getDatasetInfo(self):
        """
        返回：
        server_count: 服务器数量
        total_rows: 总数据条数
        """

        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()

        # 获取所有表名
        cur.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table'
            AND name LIKE 'server_%_metrics'
        """)

        tables = [row[0] for row in cur.fetchall()]

        server_count = len(tables)

        total_rows = 0

        # 统计每个表的数据量
        for table in tables:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            total_rows += cur.fetchone()[0]

        conn.close()

        return server_count, total_rows

    # -----------------------------
    # 对外接口
    # -----------------------------
    def genData(self, serverCount, intervalCount, anomalyRatio, start, end):
        """
        serverCount: 服务器数量
        intervalCount: 时间间隔（分钟）
        anomalyRatio: 异常比例（百分比，如 2 表示 2%）
        start/end: "2026/01/01 00:00"
        """

        start_time = self._parse_time(start)
        end_time = self._parse_time(end)

        interval = timedelta(minutes=intervalCount)

        anomaly_ratio = anomalyRatio / 100.0

        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()

        capacities = [random.uniform(0.8, 1.2) for _ in range(serverCount)]

        try:
            for i in range(serverCount):
                table = f"server_{i + 1:02d}_metrics"

                cur.execute(f"DROP TABLE IF EXISTS {table}")
                self._create_table(cur, table)

                self._generate_server(
                    cur,
                    table,
                    capacities[i],
                    start_time,
                    end_time,
                    interval,
                    anomaly_ratio
                )

            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def deleteDataByTimeRange(self, start, end):
        """
        删除所有服务器在指定时间范围内的数据
        start / end: "2026/01/01 00:00"
        """
        start_time = self._parse_time(start)
        end_time = self._parse_time(end)

        startStamp = int(start_time.timestamp())
        endStamp = int(end_time.timestamp())

        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()

        # 获取所有服务器表
        cur.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table'
            AND name LIKE 'server_%_metrics'
        """)

        tables = [row[0] for row in cur.fetchall()]

        try:
            for table in tables:
                cur.execute(
                    f"""
                    DELETE FROM {table}
                    WHERE timestamp BETWEEN ? AND ?
                    """,
                    (startStamp, endStamp)
                )

            conn.commit()
        except sqlite3.IntegrityError:
            print("删除失败")
        finally:
            conn.close()

    def getTimeRange(self):
        """
        返回数据库中最早时间和最晚时间
        格式："2026/01/01 00:00"
        """

        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()

        # 获取所有服务器表
        cur.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table'
            AND name LIKE 'server_%_metrics'
        """)

        tables = [row[0] for row in cur.fetchall()]

        global_min = None
        global_max = None

        for table in tables:
            cur.execute(f"""
                SELECT MIN(timestamp), MAX(timestamp)
                FROM {table}
            """)

            result = cur.fetchone()
            t_min, t_max = result

            # 跳过空表
            if t_min is None:
                continue

            if global_min is None or t_min < global_min:
                global_min = t_min

            if global_max is None or t_max > global_max:
                global_max = t_max

        conn.close()

        # 没有数据
        if global_min is None:
            return None, None

        # 转换格式
        start_str = datetime.fromtimestamp(global_min).strftime("%Y/%m/%d %H:%M")
        end_str = datetime.fromtimestamp(global_max).strftime("%Y/%m/%d %H:%M")

        return start_str, end_str
