from PySide6.QtCore import QObject, Slot

from manage.stream_player import StreamPlayer


class AppController(QObject):
    def __init__(self, bridge):
        super().__init__()
        self.bridge = bridge
        self.player = None

    @Slot(list)
    def on_data_ready(self, data):
        print("on_data_ready in thread OK")
        self.player = StreamPlayer(self.bridge, data)
