import numpy as np


class SequenceBuilder:
    """
    构建LSTM训练序列
    """

    def __init__(self, window_size=20):

        self.window_size = window_size

    def build(self, series):

        values = series.values

        X = []
        y = []
        ts = []

        for i in range(len(values) - self.window_size):

            window = values[i:i+self.window_size]

            target = values[i+self.window_size]

            X.append(window)

            y.append(target)

            ts.append(series.index[i+self.window_size])

        X = np.array(X)
        y = np.array(y)

        # LSTM需要三维输入
        X = X.reshape(X.shape[0], X.shape[1], 1)

        return X, y, ts
    