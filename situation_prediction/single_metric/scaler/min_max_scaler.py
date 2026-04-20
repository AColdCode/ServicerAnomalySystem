import numpy as np


class MinMaxScaler:
    def __init__(self):
        self.min = None
        self.max = None

    def fit(self, data):
        self.min = np.min(data)
        self.max = np.max(data)

    def transform(self, data):
        data = np.array(data)
        return (data - self.min) / (self.max - self.min + 1e-8)

    def inverse_transform(self, data):
        data = np.array(data)
        return data * (self.max - self.min + 1e-8) + self.min

    def state_dict(self):
        return {"min": self.min, "max": self.max}

    def load_state_dict(self, state):
        self.min = state["min"]
        self.max = state["max"]
