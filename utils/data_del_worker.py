from PySide6.QtCore import QObject, Signal


class DataDelWorker(QObject):
    finished = Signal()

    def __init__(self, generator, params):
        super().__init__()
        self.generator = generator
        self.params = params

    def run(self):
        # 执行生成
        self.generator.deleteDataByTimeRange(**self.params)

        # 完成通知
        self.finished.emit()
