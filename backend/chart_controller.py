from .stream_loader_thread import StreamLoaderThread


class ChartController:

    def __init__(self, dataManager):

        base = "results/server01"

        self.thread = StreamLoaderThread(
            dataManager,
            base
        )

    def start(self):
        self.thread.start()
