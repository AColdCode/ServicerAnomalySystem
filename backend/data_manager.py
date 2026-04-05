from PySide6.QtCore import QObject, Slot, Signal
from db.auth_manager import AuthManager
from utils.regular_match import RegularMatch


class DataManager(QObject):
    # 信号
    dataLoaded = Signal()
    loginSuccess = Signal(str, str)
    logoutSignal = Signal()

    def __init__(self):
        super().__init__()

        self.single_detect = []
        self.multi_detect = []
        self.single_predict = []
        self.multi_predict = []

        self.auth = AuthManager()
        self.current_user = None

        self.re = RegularMatch()

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
