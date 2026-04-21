from datetime import datetime
from PySide6.QtCore import QObject, Slot, Signal, Property, QThread

from db.auth_manager import AuthManager
from utils.detection_worker import DetectionWorker
from utils.regular_match import RegularMatch
from utils.user_model import UserModel
from utils.anomaly_model import AnomalyModel
from data_generator.metrics_generator import MetricsGenerator
from utils.data_gen_worker import DataGenWorker
from utils.data_del_worker import DataDelWorker
from data_source.db_reader import DBReader
from data_source.db_writer import DBWriter
from utils.trend_processor import TrendProcessor
from utils.mdetection_worker import MDetectionWorker
from utils.single_predictor_trainer_worker import SinglePredictorTrainerWorker
from utils.multi_predictor_trainer_worker import MultiPredictorTrainerWorker
from situation_prediction.single_metric.single_metric_predictor import SingleMetricPredictor
from situation_prediction.multi_metric.multi_metric_predictor import MultiMetricPredictor


class DataManager(QObject):
    # 信号
    loginSuccess = Signal(str, str)
    logoutSignal = Signal()
    userModelChanged = Signal()
    anomalyModelChanged = Signal()
    dataGenerated = Signal(int, int, str, str)
    dataDeleted = Signal(int, int, str, str)
    singleDetectUpdated = Signal(int, list, list, list, float)
    multiDetectUpdated = Signal(int, list, list, list)
    singlePredictUpdated = Signal(int, list, list, list, list)
    multiPredictUpdated = Signal(list, list, list, list, list, str)
    trendUpdated = Signal(int, list, bool, float)
    normalNumChanged = Signal(int)
    anomalyNumChanged = Signal(int)
    updateMaxMin = Signal(float, float)
    anomalyTopChanged = Signal(float, int)

    def __init__(self):
        super().__init__()
        self.auth = AuthManager()
        self.current_user = None

        self.re = RegularMatch()

        self._userModel = UserModel()
        self._anomalyModel = AnomalyModel()

        self.dbPath = "data_generator/metrics.db"
        self.gen = MetricsGenerator()
        self.interval_minutes = 5
        self.worker = None
        self.mWorker = None
        self.stPredWorker = None
        self.mtPredWorker = None
        self.genThread = None
        self.deleteTread = None

        self.dbReader = DBReader()
        self.dbWriter = DBWriter()

        self.processor = TrendProcessor()

        self.current_table = ""
        self.detectMetric = 0
        self.multiDetectMetrics = []
        self.predictMetric = 0
        self.trendRange = "1h"
        self.detectRange = "1h"
        self.multiDetectRange = "1h"
        self.predictRange = 1
        self.mPredictRange = 1
        self.endTimestamp = 0
        self.metrics = [
            "cpu_usage", "response_time", "memory_usage",
            "disk_usage", "io_read", "io_write",
            "service_rt", "service_qps"
        ]
        self.minY = 0.0
        self.maxY = 0.0

    def getUserModel(self):
        return self._userModel

    userModel = Property(QObject, getUserModel, notify=userModelChanged)

    def getAnomalyModel(self):
        return self._anomalyModel

    anomalyModel = Property(QObject, getAnomalyModel, notify=anomalyModelChanged)

    # ------------------------
    # QML接口
    # ------------------------
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

    @Slot()
    def refreshAnomalyData(self):
        range_seconds = {
            "1h": 3600,
            "6h": 21600,
            "1d": 86400,
            "7d": 604800
        }

        window = range_seconds.get(self.multiDetectRange, 3600)
        start_timestamp = self.endTimestamp - window
        res = self.dbReader.read_multi_anomaly_results(self.current_table, self.metrics,
                                                       start_timestamp, self.endTimestamp)
        self._anomalyModel.setDataList(res["data"])
        self.anomalyModelChanged.emit()
        self.anomalyTopChanged.emit(res["accuracy"] * 100, res["anomalyNum"])

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
        self.worker.finished.connect(self.mDetect)
        self.worker.finished.connect(self.singlePredictTrainer)
        self.worker.finished.connect(self.multiPredictTrainer)

        self.genThread.start()

    @Slot()
    def genFinished(self):
        server_count, total_rows = self.gen.getDatasetInfo()
        if server_count == 0:
            return
        start, end = self.gen.getTimeRange()

        self.endTimestamp = int(datetime.strptime(end, "%Y/%m/%d %H:%M").timestamp())
        self.detectMetric = 0
        self.predictMetric = 0
        self.multiDetectMetrics.append(0)
        self.setTable(0)

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
        self.get_range_data()
        self.update_all_mdata()

        self.dataDeleted.emit(server_count, total_rows, start, end)

    @Slot()
    def detect(self):
        self.worker = DetectionWorker(self.dbReader)

        self.worker.progress.connect(lambda msg: print(msg))
        self.worker.finished.connect(self.detectFinished)

        self.worker.start()

    @Slot()
    def mDetect(self):
        self.mWorker = MDetectionWorker(self.dbReader)

        self.mWorker.progress.connect(lambda msg: print(msg))
        self.mWorker.finished.connect(self.mDetectFinished)

        self.mWorker.start()

    @Slot()
    def singlePredictTrainer(self):
        self.stPredWorker = SinglePredictorTrainerWorker(self.dbReader)

        self.stPredWorker.progress.connect(lambda msg: print(msg))
        self.stPredWorker.finished.connect(self.stPredFinished)

        self.stPredWorker.start()

    @Slot()
    def multiPredictTrainer(self):
        self.mtPredWorker = MultiPredictorTrainerWorker(self.dbReader)

        self.mtPredWorker.progress.connect(lambda msg: print(msg))
        self.mtPredWorker.finished.connect(self.mtPredFinished)

        self.mtPredWorker.start()

    @Slot()
    def detectFinished(self):
        pass

    @Slot()
    def mDetectFinished(self):
        pass

    @Slot()
    def stPredFinished(self):
        pass

    @Slot()
    def mtPredFinished(self):
        pass

    @Slot(int)
    def setDetectMetric(self, metric):
        self.detectMetric = metric
        self.get_range_data()

    @Slot(int)
    def setMDetectMetric(self, metric):
        self.multiDetectMetrics.append(metric)
        self.update_all_mdata()

    @Slot(int)
    def cancelMDetectMetric(self, metric):
        self.multiDetectMetrics.remove(metric)
        self.update_all_mdata()

    @Slot(int)
    def setPredictMetric(self, metric):
        self.predictMetric = metric

    @Slot(str)
    def setTrendRange(self, r):
        self.trendRange = r
        self.update_trend()

    @Slot(str)
    def setDetectRange(self, r):
        self.detectRange = r
        self.get_range_data()

    @Slot(str)
    def setMultiDetectRange(self, r):
        self.multiDetectRange = r
        self.update_all_mdata()
        self.refreshAnomalyData()

    @Slot(int)
    def setPredictRange(self, r):
        self.predictRange = r

    @Slot(int)
    def setTable(self, tableIndex):
        tableIndex += 1
        self.current_table = f"server_{tableIndex:02d}_metrics"
        self.update_trend()
        self.get_range_data()
        self.update_all_mdata()
        self.refreshAnomalyData()

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
            value = round(values[-1], 4)
            self.trendUpdated.emit(index, trend, isAnomaly, value)
            anomalyNum += detect_anomalies.count(1)
            index += 1
        self.normalNumChanged.emit(normalNum)
        self.anomalyNumChanged.emit(anomalyNum)

    @Slot()
    def get_range_data(self):
        if self.current_table == "":
            return
        now = self.endTimestamp
        start = 0
        bucket = 0

        if self.detectRange == "1h":
            start = now - 3600
            bucket = 300

        elif self.detectRange == "6h":
            start = now - 3600 * 6
            bucket = 600

        elif self.detectRange == "1d":
            start = now - 3600 * 24
            bucket = 1800

        elif self.detectRange == "7d":
            start = now - 3600 * 24 * 7
            bucket = 7200

        timestamps, values, detect_anomalies, real_anomalies = self.dbReader.fetch_metric(self.current_table,
                                                                                          self.metrics[
                                                                                              self.detectMetric], start,
                                                                                          now)

        # 聚合
        new_ts, new_vals, new_anomalies = self.processor.aggregate(timestamps, values, detect_anomalies, bucket)

        # 计算准确率
        accCount = 0
        for i in range(len(detect_anomalies)):
            if detect_anomalies[i] == real_anomalies[i]:
                accCount += 1
        accuracy = accCount / len(detect_anomalies) * 100
        accuracy = round(accuracy, 2)

        self.singleDetectUpdated.emit(self.detectMetric, new_ts, new_vals, new_anomalies, accuracy)

    @Slot(int)
    def get_mrange_data(self, index):
        if index > 7 or index < 0:
            return
        if self.current_table == "":
            return
        now = self.endTimestamp
        start = 0
        bucket = 0
        if self.multiDetectRange == "1h":
            start = now - 3600
            bucket = 300
        elif self.multiDetectRange == "6h":
            start = now - 3600 * 6
            bucket = 600
        elif self.multiDetectRange == "1d":
            start = now - 3600 * 24
            bucket = 1800
        elif self.multiDetectRange == "7d":
            start = now - 3600 * 24 * 7
            bucket = 7200
        timestamps, values, detect_anomalies, real_anomalies = self.dbReader.fetch_metric(self.current_table,
                                                                                          self.metrics[
                                                                                              index], start,
                                                                                          now)
        new_ts, new_vals, new_anomalies = self.processor.aggregate(timestamps, values, detect_anomalies, bucket)
        max_val, min_val = max(new_vals), min(new_vals)
        if self.maxY < max_val:
            self.maxY = max_val
        if self.minY > min_val:
            self.minY = min_val
        self.multiDetectUpdated.emit(index, new_ts, new_vals, new_anomalies)

    @Slot()
    def update_all_mdata(self):
        if self.current_table == "":
            return
        self.minY = 100000.0
        self.maxY = -100000.0
        for metric in self.multiDetectMetrics:
            self.get_mrange_data(metric)
        self.updateMaxMin.emit(self.minY, self.maxY)

    @Slot(int)
    def markAnomalyHandled(self, timestamp):
        self.dbWriter.mark_anomaly_handled(self.current_table, timestamp)

    @Slot()
    def singlePredict(self):
        if self.current_table == "":
            return
        model = SingleMetricPredictor(self.metrics[self.predictMetric], self.current_table)
        preValue = model.predict_future(self.predictRange, self.interval_minutes)

        now = self.endTimestamp

        bucket = 0
        start = now - 3600 * self.predictRange

        if self.predictRange == 1:
            bucket = 300
        elif self.predictRange == 6:
            bucket = 600
        elif self.predictRange == 24:
            bucket = 1800

        timestamps, values = self.dbReader.readTimeAndMetric(self.current_table,
                                                             self.metrics[self.predictMetric], start, now)
        new_ts, new_vals = self.processor.predictAggregate(timestamps, values, bucket)

        preTimestamps = []
        for i in range(len(preValue)):
            preTimestamps.append(now + (i + 1) * self.interval_minutes * 60)
        new_preTs, new_preVals = self.processor.predictAggregate(preTimestamps, preValue, bucket)
        new_preVals = [float(x) for x in new_preVals]
        self.singlePredictUpdated.emit(self.predictMetric, new_ts, new_vals, new_preTs, new_preVals)

    @Slot()
    def multiPredict(self):
        if self.current_table == "":
            return
        model = MultiMetricPredictor(
            self.dbPath,
            self.current_table
        )
        preValues, scores, evaluate = model.predict_with_score()

        metrics_df = preValues.drop(columns=['timestamp'])
        preValues_2d = [metrics_df[col].tolist() for col in metrics_df.columns]

        new_scores = []
        for _, v in scores.items():
            new_scores.append(round(float(v), 4))

        now = self.endTimestamp
        start = now - 3600 * self.predictRange
        bucket = 300

        timestamps, values_2d = self.dbReader.readTimeAndMetrics(self.current_table,
                                                                 self.metrics, start, now)
        new_ts, new_vals_2d = self.processor.mPredictAggregate(timestamps, values_2d, bucket)

        preTimestamps = []
        for i in range(len(preValues_2d[0])):
            preTimestamps.append(now + (i + 1) * self.interval_minutes * 60)
        new_preTs, new_preVals_2d = self.processor.mPredictAggregate(preTimestamps, preValues_2d, bucket)
        self.multiPredictUpdated.emit(new_ts, new_vals_2d, new_preTs, new_preVals_2d, new_scores, evaluate)
