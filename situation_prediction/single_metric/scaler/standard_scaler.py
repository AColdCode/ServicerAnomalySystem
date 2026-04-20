import numpy as np


class StandardScaler:

    def __init__(self):
        self.mean = None
        self.std = None

    def fit(self, data):
        data = np.array(data)
        self.mean = np.mean(data)
        self.std = np.std(data)

    def transform(self, data):
        data = np.array(data)
        return (data - self.mean) / (self.std + 1e-8)

    def inverse_transform(self, data):
        data = np.array(data)
        return data * (self.std + 1e-8) + self.mean

    def state_dict(self):
        return {
            "mean": self.mean,
            "std": self.std
        }

    def load_state_dict(self, state):
        self.mean = state["mean"]
        self.std = state["std"]
