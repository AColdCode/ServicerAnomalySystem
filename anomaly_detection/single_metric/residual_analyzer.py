import numpy as np


class ResidualAnalyzer:

    def __init__(self):

        self.residual_history = []

    def compute_residual(self, value, predict):

        residual = value - predict

        self.residual_history.append(residual)

        if len(self.residual_history) > 288:
            self.residual_history.pop(0)

        return residual

    def compute_zscore(self, residual):

        if len(self.residual_history) < 30:
            return 0

        mean = np.mean(self.residual_history)

        std = np.std(self.residual_history)

        std = max(std, 1)

        z = (residual - mean) / std

        return z

    def compute_mad_score(self, residual):

        if len(self.residual_history) < 30:
            return 0

        median = np.median(self.residual_history)

        abs_dev = [abs(x - median) for x in self.residual_history]

        mad = np.median(abs_dev)

        mad = max(mad, 1e-6)

        score = abs(residual - median) / (1.4826 * mad)

        return score
