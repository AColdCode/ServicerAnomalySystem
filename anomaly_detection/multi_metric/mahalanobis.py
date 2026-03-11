import numpy as np


class MahalanobisDistance:
    """
    计算Mahalanobis距离
    """

    def __init__(self):

        self.mean = None
        self.inv_cov = None

    def fit(self, X):

        self.mean = np.mean(X, axis=0)

        cov = np.cov(X, rowvar=False)

        self.inv_cov = np.linalg.pinv(cov)

    def distance(self, x):

        delta = x - self.mean

        d = np.sqrt(delta @ self.inv_cov @ delta.T)

        return d

    def batch_distance(self, X):

        distances = []

        for x in X:

            d = self.distance(x)

            distances.append(d)

        return np.array(distances)