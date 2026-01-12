# anomaly_model.py
import random
from config import Config

ANOMALY_TYPES = [
    "CPU_PRESSURE",
    "SERVICE_LATENCY",
    "IO_BOTTLENECK"
]


class AnomalyEvent:
    def __init__(self, kind, length):
        self.kind = kind  # 异常类型
        self.length = length  # 持续长度
        self.pos = 0  # 当前进度

    def step(self):
        self.pos += 1
        return self.pos <= self.length


class AnomalyController:
    def __init__(self):
        self.current_event = None
        self.total = Config.TOTAL_POINTS
        self.abnormal = 0
        self.target_ratio = random.uniform(0.01, 0.03)

    def next_event(self):
        # 正在异常中
        if self.current_event:
            active = self.current_event.step()
            if active:
                self.abnormal += 1
                return self.current_event
            else:
                self.current_event = None
                return None

        # 已达到异常比例上限
        if self.abnormal / self.total >= self.target_ratio:
            return None

        # 触发新异常
        if random.random() < 0.01:
            kind = random.choice(ANOMALY_TYPES)
            length = random.randint(
                Config.ANOMALY_MIN_LEN,
                Config.ANOMALY_MAX_LEN
            )
            self.current_event = AnomalyEvent(kind, length)
            self.abnormal += 1
            return self.current_event

        return None
