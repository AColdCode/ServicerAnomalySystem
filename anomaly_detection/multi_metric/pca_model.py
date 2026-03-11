import numpy as np


class PCA:
    """
    PCA降维模型
    """

    def __init__(self, n_components=None):

        self.n_components = n_components

        self.mean = None
        self.components = None
        self.eigenvalues = None

    def fit(self, X):

        # 中心化
        self.mean = np.mean(X, axis=0)

        X_centered = X - self.mean

        # 协方差矩阵
        cov = np.cov(X_centered, rowvar=False)

        # 特征分解
        eigenvalues, eigenvectors = np.linalg.eigh(cov)

        # 排序
        idx = np.argsort(eigenvalues)[::-1]

        eigenvalues = eigenvalues[idx]

        eigenvectors = eigenvectors[:, idx]

        if self.n_components:

            eigenvectors = eigenvectors[:, :self.n_components]
            eigenvalues = eigenvalues[:self.n_components]

        self.components = eigenvectors
        self.eigenvalues = eigenvalues

    def transform(self, X):

        X_centered = X - self.mean

        return np.dot(X_centered, self.components)

    def fit_transform(self, X):

        self.fit(X)

        return self.transform(X)