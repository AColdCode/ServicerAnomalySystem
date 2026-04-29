import os
import sys

from PySide6.QtCore import qInstallMessageHandler
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication

from backend.data_manager import DataManager

os.environ["QT_LOGGING_RULES"] = "qt.qml.debug=true"
os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"


def qt_message_handler(mode, context, message):
    print(f"[QML] {message}")


qInstallMessageHandler(qt_message_handler)


def main():
    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()

    # 数据管理器
    dataManager = DataManager()

    engine.rootContext().setContextProperty(
        "DataManager",
        dataManager
    )

    # 加载UI
    engine.load("ui/Main.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
