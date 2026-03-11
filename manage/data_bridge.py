# data_bridge.py
from PySide6.QtCore import QObject, Signal, Slot


class DataBridge(QObject):
    # 定义QML监听的newPoint信号（参数类型要和QML匹配）
    newPoint = Signal(float, float, int)  # ts(秒级), value, isAnomaly

    def __init__(self):
        super().__init__()

    # 发送数据点的方法（触发信号）
    def send_point(self, ts, value, is_anomaly):
        # 触发信号（QML的onNewPoint会接收）
        self.newPoint.emit(ts, value, is_anomaly)
