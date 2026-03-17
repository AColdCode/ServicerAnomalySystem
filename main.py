import sys
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl, qInstallMessageHandler, QThread, Qt
from manage.data_loader import DataLoader

from manage.data_bridge import DataBridge
from manage.controller import AppController
from manage.config import *

os.environ["QT_LOGGING_RULES"] = "qt.qml.debug=true"


def qt_message_handler(mode, context, message):
    print(f"[QML] {message}")


qInstallMessageHandler(qt_message_handler)
app = QApplication(sys.argv)

bridge = DataBridge()
controller = AppController(bridge)

engine = QQmlApplicationEngine()

# 暴露给 QML
engine.rootContext().setContextProperty("dataBridge", bridge)

qml_path = os.path.abspath("qml/MainView.qml")
engine.load(QUrl.fromLocalFile(qml_path))

if not engine.rootObjects():
    print("Failed to load QML")
    sys.exit(-1)

# ===============================
# 后台加载线程
# ===============================
thread = QThread()
loader = DataLoader(DATA_DIR + "sever01/cpu_usage_detect.csv")

loader.moveToThread(thread)

thread.started.connect(loader.load)
loader.finished.connect(thread.quit)
loader.finished.connect(loader.deleteLater)
thread.finished.connect(thread.deleteLater)
player = None

loader.finished.connect(controller.on_data_ready, Qt.QueuedConnection)

thread.start()

sys.exit(app.exec())
