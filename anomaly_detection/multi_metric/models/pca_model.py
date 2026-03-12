import numpy as np


class PCAModel:
    """
    工业级 PCA 模型

    功能：
    1 训练 PCA
    2 主成分选择
    3 投影
    4 重构
    """

    def __init__(self, variance_ratio=0.9):

        # 主成分累计贡献率
        self.variance_ratio = variance_ratio

        # PCA参数
        self.mean = None
        self.std = None

        self.eigenvalues = None
        self.eigenvectors = None

        self.components = None

        self.k = None

    # =========================
    # 标准化
    # =========================

    def _standardize(self, X):

        self.mean = np.mean(X, axis=0)
        self.std = np.std(X, axis=0)

        self.std[self.std == 0] = 1e-8

        X_norm = (X - self.mean) / self.std

        return X_norm

    # =========================
    # 协方差矩阵
    # =========================

    def _cov_matrix(self, X):

        n = X.shape[0]

        cov = np.dot(X.T, X) / (n - 1)

        return cov

    # =========================
    # 特征值分解
    # =========================

    def _eigen_decomposition(self, cov):

        eigenvalues, eigenvectors = np.linalg.eig(cov)

        idx = np.argsort(eigenvalues)[::-1]

        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        return eigenvalues, eigenvectors

    # =========================
    # 选择主成分
    # =========================

    def _select_components(self, eigenvalues):

        total = np.sum(eigenvalues)

        ratio = eigenvalues / total

        cum_ratio = np.cumsum(ratio)

        k = np.searchsorted(cum_ratio, self.variance_ratio) + 1

        return k

    # =========================
    # 训练 PCA
    # =========================

    def fit(self, X):

        """
        训练PCA
        """

        # 标准化
        X_norm = self._standardize(X)

        # 协方差矩阵
        cov = self._cov_matrix(X_norm)

        # 特征分解
        eigenvalues, eigenvectors = self._eigen_decomposition(cov)

        self.eigenvalues = eigenvalues
        self.eigenvectors = eigenvectors

        # 选择主成分
        k = self._select_components(eigenvalues)

        self.k = k

        self.components = eigenvectors[:, :k]

    # =========================
    # 数据标准化（预测用）
    # =========================

    def transform(self, X):

        X_norm = (X - self.mean) / self.std

        return X_norm

    # =========================
    # 投影
    # =========================

    def project(self, X):

        X_norm = self.transform(X)

        T = np.dot(X_norm, self.components)

        return T

    # =========================
    # 重构
    # =========================

    def reconstruct(self, X):

        X_norm = self.transform(X)

        T = np.dot(X_norm, self.components)

        X_hat = np.dot(T, self.components.T)

        return X_hat

    # =========================
    # 获取特征值
    # =========================

    def get_eigenvalues(self):

        return self.eigenvalues[:self.k]