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
# | is_anomaly    | 整体是否异常      | 0 / 1               |

import sqlite3
import random
import math
from datetime import datetime, timedelta

DB_NAME = "metrics.db"

START_TIME = datetime(2025, 9, 1)
END_TIME = datetime(2026, 3, 1)

INTERVAL = timedelta(minutes=5)

SERVER_NUM = 10

ANOMALY_RATIO = 0.02


# -----------------------------
# 周期函数
# -----------------------------
def day_cycle(t):
    seconds = t.hour * 3600 + t.minute * 60

    return math.sin(2 * math.pi * seconds / 86400)


def week_cycle(t):
    return math.sin(2 * math.pi * t.weekday() / 7)


def noise(scale):
    return random.uniform(-scale, scale)


# -----------------------------
# 业务负载
# -----------------------------
def generate_load(t, capacity):
    base = 60 * capacity

    daily = 25 * day_cycle(t)

    weekly = 12 * week_cycle(t)

    load = base + daily + weekly + noise(4)

    return max(load, 5)


# -----------------------------
# 指标生成
# -----------------------------
def generate_metrics(load, capacity):
    qps = load

    cpu = 0.004 + load * 0.00009 / capacity + noise(0.001)

    rt = 0.05 + load * 0.0012 + noise(0.01)

    srt = rt * (1 + noise(0.05))

    mem = 3 + load * 0.06 + noise(0.5)

    read = 30 + load * 0.9 + noise(5)

    write = 20 + load * 0.6 + noise(4)

    disk = 10 + (read + write) * 0.01 + noise(0.4)

    return cpu, rt, mem, disk, read, write, srt, qps


# -----------------------------
# 异常传播模型
# -----------------------------
def propagate(cpu, rt, mem, disk, read, write, srt, qps, amp, anomaly_type):
    cpu_flag = rt_flag = mem_flag = disk_flag = 0
    read_flag = write_flag = srt_flag = qps_flag = 0

    if anomaly_type == "cpu":

        cpu *= amp * 4
        rt *= amp
        qps *= 0.7

        cpu_flag = 1
        rt_flag = 1

    elif anomaly_type == "response":

        rt *= amp * 5
        srt = rt
        qps *= 0.6

        rt_flag = 1
        srt_flag = 1

    elif anomaly_type == "memory":

        mem *= amp * 3
        mem_flag = 1

    elif anomaly_type == "disk":

        disk *= amp * 3
        disk_flag = 1

    elif anomaly_type == "io_read":

        read *= amp * 5
        disk *= amp

        read_flag = 1
        disk_flag = 1

    elif anomaly_type == "io_write":

        write *= amp * 5
        disk *= amp

        write_flag = 1
        disk_flag = 1

    elif anomaly_type == "service_rt":

        srt *= amp * 5
        rt = srt
        qps *= 0.5

        srt_flag = 1
        rt_flag = 1

    elif anomaly_type == "qps":

        qps *= amp * 3
        cpu *= amp
        rt *= amp

        qps_flag = 1
        cpu_flag = 1
        rt_flag = 1

    return (
        cpu, rt, mem, disk, read, write, srt, qps,
        cpu_flag, rt_flag, mem_flag, disk_flag,
        read_flag, write_flag, srt_flag, qps_flag
    )


# -----------------------------
# 创建表
# -----------------------------
def create_table(cur, table):
    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS {table}(
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
# 数据生成
# -----------------------------
def generate_server(cur, table, capacity):
    t = START_TIME

    anomaly_left = 0
    anomaly_len = 0
    anomaly_type = None

    cooldown = 0

    memory_leak = False
    leak_step = 0

    while t < END_TIME:

        load = generate_load(t, capacity)

        cpu, rt, mem, disk, read, write, srt, qps = generate_metrics(load, capacity)

        cpu_flag = rt_flag = mem_flag = disk_flag = 0
        read_flag = write_flag = srt_flag = qps_flag = 0

        root_cause = "normal"

        if anomaly_left == 0 and cooldown == 0:

            if random.random() < ANOMALY_RATIO:
                anomaly_type = random.choice([
                    "cpu", "response", "memory",
                    "disk", "io_read", "io_write",
                    "service_rt", "qps"
                ])

                anomaly_len = random.randint(3, 12)

                anomaly_left = anomaly_len

        if anomaly_left > 0:

            step = anomaly_len - anomaly_left + 1

            amp = 1 + 3 * math.sin(math.pi * step / anomaly_len)

            (
                cpu, rt, mem, disk, read, write, srt, qps,
                cpu_flag, rt_flag, mem_flag, disk_flag,
                read_flag, write_flag, srt_flag, qps_flag
            ) = propagate(
                cpu, rt, mem, disk, read, write, srt, qps,
                amp, anomaly_type
            )

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

            mem_flag = 1
            root_cause = "memory_leak"

            leak_step += 1

            if leak_step > random.randint(24, 48):
                memory_leak = False

        is_anomaly = int(
            cpu_flag or rt_flag or mem_flag or disk_flag
            or read_flag or write_flag or srt_flag or qps_flag
        )

        cur.execute(
            f"""
            INSERT INTO {table}(
                timestamp,
                cpu_usage,
                response_time,
                memory_usage,
                disk_usage,
                io_read,
                io_write,
                service_rt,
                service_qps,

                is_anomaly,

                cpu_anomaly,
                response_time_anomaly,
                memory_anomaly,
                disk_anomaly,
                io_read_anomaly,
                io_write_anomaly,
                service_rt_anomaly,
                service_qps_anomaly,

                root_cause
            )
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                int(t.timestamp()),
                cpu, rt, mem, disk, read, write, srt, qps,

                is_anomaly,

                cpu_flag,
                rt_flag,
                mem_flag,
                disk_flag,
                read_flag,
                write_flag,
                srt_flag,
                qps_flag,

                root_cause
            )
        )

        t += INTERVAL


# -----------------------------
# 主函数
# -----------------------------
def main():
    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

    capacities = [random.uniform(0.8, 1.2) for _ in range(SERVER_NUM)]

    for i in range(1, SERVER_NUM + 1):
        table = f"server_{i:02d}_metrics"

        print("Generating", table)

        cur.execute(f"DROP TABLE IF EXISTS {table}")

        create_table(cur, table)

        generate_server(cur, table, capacities[i - 1])

        conn.commit()

    conn.close()

    print("Dataset generation completed.")


if __name__ == "__main__":
    main()
