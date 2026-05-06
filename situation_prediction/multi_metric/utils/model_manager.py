import sys

import torch
import os


class ModelManager:

    @staticmethod
    def save(model, path):
        base_path = os.path.abspath(".")
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        os.makedirs(base_path, os.path.dirname(path), exist_ok=True)
        path = os.path.join(base_path, path)

        torch.save(model.state_dict(), path)

    @staticmethod
    def load(model, path):
        base_path = os.path.abspath(".")
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        path = os.path.join(base_path, path)
        model.load_state_dict(torch.load(path))

        model.eval()

        return model
    