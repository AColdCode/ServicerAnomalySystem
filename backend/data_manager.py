from datetime import datetime
from PySide6.QtCore import QObject, Slot, Signal, Property, QThread

from db.auth_manager import AuthManager
from utils.detection_worker import DetectionWorker
from utils.regular_match import RegularMatch
from utils.user_model import UserModel
from data_generator.metrics_generator import MetricsGenerator
from utils.data_gen_worker import DataGenWorker
from utils.data_del_worker import DataDelWorker
from data_source.db_reader import DBReader
from utils.trend_processor import TrendProcessor


class DataManager(QObject):
    # 信号
    dataLoaded = Signal()
    loginSuccess = Signal(str, str)
    logoutSignal = Signal()
    userModelChanged = Signal()
    dataGenerated = Signal(int, int, str, str)
    dataDeleted = Signal(int, int, str, str)
    detectUpdated = Signal(int, list)
    predictUpdated = Signal(int, list)
    trendUpdated = Signal(int, list, bool, float)
    normalNumChanged = Signal(int)
    anomalyNumChanged = Signal(int)

    def __init__(self):
        super().__init__()

        self.single_detect = []
        self.multi_detect = []
        self.single_predict = []
        self.multi_predict = []

        self.auth = AuthManager()
        self.current_user = None

        self.re = RegularMatch()

        self._userModel = UserModel()

        self.gen = MetricsGenerator()
        self.worker = None
        self.genThread = None
        self.deleteTread = None
        self.detectThread = None

        self.dbReader = DBReader()

        self.processor = TrendProcessor()

        self.current_table = ""
        self.detectMetric = 0
        self.predictMetric = 0
        self.trendRange = "1h"
        self.detectRange = "1h"
        self.predictRange = "1h"
        self.endTimestamp = 0
        self.metrics = [
            "cpu_usage", "response_time", "memory_usage",
            "disk_usage", "io_read", "io_write",
            "service_rt", "service_qps"
        ]

    def getUserModel(self):
        return self._userModel

    userModel = Property(QObject, getUserModel, notify=userModelChanged)

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

    @Slot(str, str, result=str)
    def login(self, username, password):
        role = self.auth.login(username, password)
        if role:
            self.current_user = {
                "username": username,
                "role": role
            }
            self.loginSuccess.emit(username, role)
            return role
        return ""

    @Slot(str, str, result=bool)
    def register(self, username, password, role="user"):
        role = self.auth.register(username, password, role)
        if role:
            self.current_user = {
                "username": username,
                "role": role
            }
            self.loginSuccess.emit(username, role)

        return bool(role)

    @Slot(str, result=bool)
    def isLegalUsername(self, username):
        return self.re.isLegalUsername(username)

    @Slot(str, result=bool)
    def isLegalPassword(self, password):
        return self.re.isLegalPassword(password)

    @Slot()
    def logout(self):
        self.current_user = None
        self.logoutSignal.emit()

    @Slot()
    def refreshUsers(self):
        users = self.auth.get_all_users()

        # 防止 NULL
        for u in users:
            u["username"] = u.get("username") or ""
            u["role"] = u.get("role") or ""
            u["created_at"] = u.get("created_at") or ""
            u["is_active"] = u.get("is_active") if u.get("is_active") is not None else 0
            u["parent_admin"] = u.get("parent_admin") or ""

        self._userModel.setUsers(users)
        self.userModelChanged.emit()

    @Slot(str, str, result=bool)
    def changeUserRole(self, username, role):
        name, _role = self.current_user
        if _role == "user":
            return False
        return self.auth.change_user_role(username, role, name)

    @Slot(str, str, result=bool)
    def changeUserActive(self, username, active):
        name, role = self.current_user
        if role == "user":
            return False
        return self.auth.change_user_active(username, active, name)

    @Slot(str, result=bool)
    def deleteUser(self, username):
        name, role = self.current_user
        if role == "user":
            return False
        return self.auth.delete_user(username, name)

    @Slot(int, int, int, str, str)
    def genData(self, serverCount, intervalCount, anomalyRatio, start, end):
        params = {
            "serverCount": serverCount,
            "intervalCount": intervalCount,
            "anomalyRatio": anomalyRatio,
            "start": start,
            "end": end
        }
        self.genThread = QThread()
        self.worker = DataGenWorker(self.gen, params)

        # 移动到子线程
        self.worker.moveToThread(self.genThread)

        self.genThread.started.connect(self.worker.run)

        self.worker.finished.connect(self.genThread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.genThread.finished.connect(self.genThread.deleteLater)
        self.worker.finished.connect(self.genFinished)
        self.worker.finished.connect(self.detect)

        self.genThread.start()

    @Slot()
    def genFinished(self):
        server_count, total_rows = self.gen.getDatasetInfo()
        if server_count == 0:
            return

        start, end = self.gen.getTimeRange()

        self.endTimestamp = int(datetime.strptime(end, "%Y/%m/%d %H:%M").timestamp())
        self.setTable(0)
        self.setDetectMetric(0)
        self.setPredictMetric(0)

        self.dataGenerated.emit(server_count, total_rows, start, end)

    @Slot(str, str)
    def deleteDataset(self, start, end):
        params = {
            "start": start,
            "end": end
        }
        self.deleteTread = QThread()
        self.worker = DataDelWorker(self.gen, params)

        # 移动到子线程
        self.worker.moveToThread(self.deleteTread)

        self.deleteTread.started.connect(self.worker.run)

        self.worker.finished.connect(self.deleteTread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.deleteTread.finished.connect(self.deleteTread.deleteLater)
        self.worker.finished.connect(self.delFinished)

        self.deleteTread.start()

    @Slot()
    def delFinished(self):
        server_count, total_rows = self.gen.getDatasetInfo()
        if server_count == 0:
            return

        start, end = self.gen.getTimeRange()
        self.endTimestamp = int(datetime.strptime(end, "%Y/%m/%d %H:%M").timestamp())
        self.update_trend()

        self.dataDeleted.emit(server_count, total_rows, start, end)

    @Slot()
    def detect(self):
        self.worker = DetectionWorker(self.dbReader)

        self.worker.progress.connect(lambda msg: print(msg))
        self.worker.finished.connect(self.detectFinished)

        self.worker.start()

    @Slot()
    def detectFinished(self):
        pass

    @Slot(str)
    def setDetectMetric(self, metric):
        self.detectMetric = metric

    @Slot(str)
    def setPredictMetric(self, metric):
        self.predictMetric = metric

    @Slot(str)
    def setTrendRange(self, r):
        self.trendRange = r
        self.update_trend()

    @Slot(str)
    def setDetectRange(self, r):
        self.detectRange = r

    @Slot(str)
    def setPredictRange(self, r):
        self.predictRange = r

    @Slot(int)
    def setTable(self, tableIndex):
        tableIndex += 1
        self.current_table = f"server_{tableIndex:02d}_metrics"
        self.update_trend()

    @Slot()
    def update_trend(self):
        if self.current_table == "":
            return
        index = 0
        normalNum = 0
        anomalyNum = 0
        for metric in self.metrics:
            range_seconds = {
                "1h": 3600,
                "6h": 21600,
                "1d": 86400,
                "7d": 604800
            }

            window = range_seconds.get(self.trendRange, 3600)
            start_timestamp = self.endTimestamp - window
            timestamps, values, detect_anomalies, real_anomalies = self.dbReader.fetch_metric(
                self.current_table,
                metric,
                start_timestamp,
                self.endTimestamp
            )

            if 1 in detect_anomalies:
                isAnomaly = True
            else:
                isAnomaly = False
                normalNum += 1

            if not timestamps:
                return

            trend = self.processor.generate_trend(timestamps, values, real_anomalies, self.trendRange)
            value = round(values[-1], 3)
            self.trendUpdated.emit(index, trend, isAnomaly, value)
            anomalyNum += detect_anomalies.count(1)
            index += 1
        self.normalNumChanged.emit(normalNum)
        self.anomalyNumChanged.emit(anomalyNum)
