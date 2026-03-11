from PySide6.QtCore import QTimer, QObject


class StreamPlayer:
    def __init__(self, bridge, data):
        self.bridge = bridge
        self.data = data
        self.index = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.push_batch)
        self.timer.start(500)  # 播放速度

    def push_batch(self):
        BATCH = 5

        if self.index >= len(self.data):
            self.timer.stop()
            return

        end = min(self.index + BATCH, len(self.data))

        for i in range(self.index, end):
            ts, v, a = self.data[i]
            self.bridge.send_point(ts, v, a)

        self.index = end
