import torch
import os


class ModelManager:

    @staticmethod
    def save(model, path):

        os.makedirs(os.path.dirname(path), exist_ok=True)

        torch.save(model.state_dict(), path)

    @staticmethod
    def load(model, path):

        model.load_state_dict(torch.load(path))

        model.eval()

        return model
    