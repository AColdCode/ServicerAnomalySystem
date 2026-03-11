# server_generator.py
import time
from metric_model import MetricModel
from anomaly_model import AnomalyController
from config import Config


class ServerGenerator:
    def __init__(self, server_id, db):
        self.server_id = server_id
        self.db = db
        self.anomaly = AnomalyController()
        self.metric = MetricModel()
        self.table = f"server_{server_id:02d}_metrics"

    def run(self):
        start_ts = int(time.time()) - Config.TOTAL_POINTS * Config.SAMPLE_INTERVAL_SEC

        for t in range(Config.TOTAL_POINTS):
            ts = start_ts + t * Config.SAMPLE_INTERVAL_SEC

            event = self.anomaly.next_event()

            metrics = self.metric.generate(t, event)

            record = (
                ts,
                *metrics,
                int(event is not None)
            )

            self.db.insert(self.table, record)

        self.db.commit()
