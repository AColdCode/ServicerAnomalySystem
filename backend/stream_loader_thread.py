from PySide6.QtCore import QThread

from .fast_csv_loader import FastCSVLoader


class StreamLoaderThread(QThread):

    def __init__(self, dataManager, basePath):
        super().__init__()

        self.dataManager = dataManager
        self.basePath = basePath

        self.loader = FastCSVLoader()

    def run(self):

        # 单指标异常
        rows = self.loader.load(self.basePath + "/cpu_usage_detect.csv")
        data = self.loader.parse_single_detect(rows)
        self.dataManager.setSingleDetect(data)

        # 多指标异常
        rows = self.loader.load(self.basePath + "/pca_detect.csv")
        data = self.loader.parse_multi_detect(rows)
        self.dataManager.setMultiDetect(data)

        # 单指标预测
        rows = self.loader.load(self.basePath + "/cpu_prediction.csv")
        data = self.loader.parse_single_predict(rows)
        self.dataManager.setSinglePredict(data)

        # 多指标预测
        rows = self.loader.load(self.basePath + "/lstm_prediction.csv")
        data = self.loader.parse_multi_predict(rows)
        self.dataManager.setMultiPredict(data)

        # 通知UI
        self.dataManager.notifyLoaded()
