import numpy as np


class MultiStandardScaler:

    def __init__(self):
        self.mean = None
        self.std = None

    def fit(self, data):
        data = np.array(data)

        # 按列计算
        self.mean = np.mean(data, axis=0)
        self.std = np.std(data, axis=0)

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

    def inverse_transform_partial(self, data):
        """
        只对前N维做反归一化（用于预测输出）
        data: (steps, feature_dim=8)
        """
        mean = self.mean[:data.shape[1]]
        std = self.std[:data.shape[1]]

        return data * (std + 1e-8) + mean
