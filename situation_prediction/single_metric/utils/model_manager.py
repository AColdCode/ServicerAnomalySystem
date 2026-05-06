import sys

import torch
import os


class ModelManager:

    def __init__(self, model_dir="single_models"):

        self.model_dir = model_dir

        if not os.path.exists(model_dir):

            os.makedirs(model_dir)

    def save(self, model, table, name):
        base_path = os.path.abspath(".")
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        os.makedirs(os.path.join(base_path, self.model_dir, table), exist_ok=True)
        path = os.path.join(base_path, self.model_dir, table, name + ".pth")

        torch.save(model.state_dict(), path)

        print("模型已保存:", path)

    def load(self, model, table, name):
        base_path = os.path.abspath(".")
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        indirect_path = os.path.join(self.model_dir, table, name + ".pth")
        path = os.path.join(base_path, indirect_path)

        model.load_state_dict(torch.load(path))

        model.eval()

        print("模型已加载:", path)

        return model
    