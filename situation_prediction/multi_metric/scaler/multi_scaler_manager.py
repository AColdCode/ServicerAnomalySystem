import os
import sys

import joblib


class MultiScalerManager:

    def __init__(self, base_dir="scalers"):
        self.base_dir = base_dir

    def _dir(self, table):
        path = os.path.join(self.base_dir, table)
        os.makedirs(path, exist_ok=True)
        return path

    def _path(self, table):
        base_path = os.path.abspath(".")
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        scaler_dir = os.path.join(self._dir(table), "multi_scaler.pkl")
        path = os.path.join(base_path, scaler_dir)
        return path

    def save(self, scaler, table):
        joblib.dump(scaler.state_dict(), self._path(table))

    def load(self, table):
        path = self._path(table)

        if not os.path.exists(path):
            raise Exception(f"Scaler不存在: {path}")

        return joblib.load(path)
