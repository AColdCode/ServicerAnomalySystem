import os

import joblib


class MultiScalerManager:

    def __init__(self, base_dir="scalers"):
        self.base_dir = base_dir

    def _dir(self, table):
        path = os.path.join(self.base_dir, table)
        os.makedirs(path, exist_ok=True)
        return path

    def _path(self, table):
        return os.path.join(self._dir(table), "multi_scaler.pkl")

    def save(self, scaler, table):
        joblib.dump(scaler.state_dict(), self._path(table))

    def load(self, table):
        path = self._path(table)

        if not os.path.exists(path):
            raise Exception(f"Scaler不存在: {path}")

        return joblib.load(path)
