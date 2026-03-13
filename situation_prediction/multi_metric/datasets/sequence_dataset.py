import numpy as np


class SequenceDataset:
    """
    时间序列样本生成器
    """

    def __init__(self, seq_len, pred_len):

        self.seq_len = seq_len
        self.pred_len = pred_len

    def create_sequences(self, data):

        X = []
        Y = []

        total = len(data)

        for i in range(total - self.seq_len - self.pred_len):

            x = data[i:i + self.seq_len]

            y = data[i + self.seq_len:i + self.seq_len + self.pred_len]

            X.append(x)

            Y.append(y)

        return np.array(X), np.array(Y)
    