from PySide6.QtCore import QObject, Slot, Signal


class DataManager(QObject):

    dataLoaded = Signal()

    def __init__(self):
        super().__init__()

        self.single_detect = []
        self.multi_detect = []
        self.single_predict = []
        self.multi_predict = []

    # ------------------------
    # python内部调用
    # ------------------------

    def setSingleDetect(self, d):
        self.single_detect = d

    def setMultiDetect(self, d):
        self.multi_detect = d

    def setSinglePredict(self, d):
        self.single_predict = d

    def setMultiPredict(self, d):
        self.multi_predict = d

    def notifyLoaded(self):
        self.dataLoaded.emit()

    # ------------------------
    # QML接口
    # ------------------------

    @Slot(str, result="QVariantList")
    def getSingle(self, mode):

        if mode == "detect":
            return self.single_detect

        if mode == "predict":
            return self.single_predict

        return []

    @Slot(str, result="QVariantList")
    def getMulti(self, mode):

        if mode == "detect":
            return self.multi_detect

        if mode == "predict":
            return self.multi_predict

        return []
