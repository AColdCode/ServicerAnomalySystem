from PySide6.QtCore import QThread, Signal
from concurrent.futures import ThreadPoolExecutor, as_completed
from situation_prediction.single_metric.single_metric_predictor_trainer import SingleMetricPredictorTrainer


class SinglePredictorTrainerWorker(QThread):
    progress = Signal(str)
    finished = Signal()

    def __init__(self, dbReader):
        super().__init__()
        self.dbReader = dbReader

    def run(self):

        DB_PATH = "data_generator/metrics.db"
        tables = self.dbReader.get_server_tables()

        metrics = [
            "cpu_usage", "response_time", "memory_usage",
            "disk_usage", "io_read", "io_write",
            "service_rt", "service_qps"
        ]

        tasks = []

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(self.run_single_task, DB_PATH, table, metric)
                for table in tables
                for metric in metrics
            ]

            for future in as_completed(futures):
                result = future.result()
                self.progress.emit(result)

        self.finished.emit()

    def run_single_task(self, db_path, table, metric):
        try:
            service = SingleMetricPredictorTrainer(
                db_path,
                table,
                metric
            )
            service.train_and_save()
            return f"[OK] {table} - {metric}"
        except Exception as e:
            return f"[ERROR] {table} - {metric}: {str(e)}"
