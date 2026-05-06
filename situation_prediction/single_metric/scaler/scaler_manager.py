import sys

import joblib
import os


class ScalerManager:
    def __init__(self, base_dir="scalers"):
        self.base_dir = base_dir

    # =========================
    # 路径结构：table/metric.pkl
    # =========================
    def _dir(self, table):
        os.makedirs(os.path.join(self.base_dir, table), exist_ok=True)
        return os.path.join(self.base_dir, table)

    def _path(self, table, metric):
        base_path = os.path.abspath(".")
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        scaler_dir = os.path.join(self._dir(table), f"{metric}.pkl")
        path = os.path.join(base_path, scaler_dir)
        return path

    # =========================
    # save
    # =========================
    def save(self, scaler, table, metric):
        dir_path = self._dir(table)
        os.makedirs(dir_path, exist_ok=True)

        joblib.dump(
            scaler.state_dict(),
            self._path(table, metric)
        )

    # =========================
    # load
    # =========================
    def load(self, table, metric):
        path = self._path(table, metric)

        if not os.path.exists(path):
            raise Exception(f"Scaler不存在: {path}")

        state = joblib.load(path)

        return state
