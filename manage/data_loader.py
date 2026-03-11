from PySide6.QtCore import QObject, Signal, Slot, QDateTime
import csv


class DataLoader(QObject):
    finished = Signal(list)  # ⭐ 数据加载完成
    progress = Signal(int)   # （可选）进度

    def __init__(self, csv_path):
        super().__init__()
        self.csv_path = csv_path

    @Slot()
    def load(self):
        data = []

        with open(self.csv_path, newline="") as f:
            reader = csv.DictReader(f)

            for i, row in enumerate(reader):
                dt = QDateTime.fromString(
                    row["timestamp"], "yyyy-MM-dd HH:mm:ss"
                )
                ts = dt.toMSecsSinceEpoch()
                value = float(row["cpu_usage"])
                is_anomaly = int(row["cpu_usage_anomaly"] == "True")

                data.append((ts, value, is_anomaly))

                # （可选）每1000条发一次进度
                if i % 1000 == 0:
                    self.progress.emit(i)

        self.finished.emit(data)