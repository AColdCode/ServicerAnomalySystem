from PySide6.QtCore import QThread, Signal
from concurrent.futures import ThreadPoolExecutor, as_completed
from situation_prediction.multi_metric.multi_metric_predictor_trainer import MultiMetricPredictorTrainer


class MultiPredictorTrainerWorker(QThread):
    progress = Signal(str)
    finished = Signal()

    def __init__(self, dbReader):
        super().__init__()
        self.dbReader = dbReader

    def run(self):

        DB_PATH = r"D:\Python\pythonProject\ServicerAnomalySystem\data_generator\metrics.db"
        tables = self.dbReader.get_server_tables()

        tasks = []

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(self.run_single_task, DB_PATH, table)
                for table in tables
            ]

            for future in as_completed(futures):
                result = future.result()
                self.progress.emit(result)

        self.finished.emit()

    def run_single_task(self, db_path, table):
        try:
            service = MultiMetricPredictorTrainer(
                db_path,
                table
            )
            service.train_and_save()
            return f"[OK] {table}"
        except Exception as e:
            return f"[ERROR] {table}: {str(e)}"
