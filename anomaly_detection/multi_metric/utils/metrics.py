import numpy as np


class PCAMetrics:
    """
    PCA异常检测统计量计算

    包含：
    1 SPE统计量
    2 Hotelling T²统计量
    """

    def __init__(self, pca_model):

        self.model = pca_model

        # 主成分特征值
        self.eigenvalues = pca_model.get_eigenvalues()

    # =================================
    # SPE 计算
    # =================================

    def spe(self, X):

        """
        计算 Squared Prediction Error

        SPE = ||X - X_hat||²
        """

        X_norm = self.model.transform(X)

        T = np.dot(X_norm, self.model.components)

        X_hat = np.dot(T, self.model.components.T)

        residual = X_norm - X_hat

        spe = np.sum(residual ** 2, axis=1)

        return spe

    # =================================
    # 单样本 SPE
    # =================================

    def spe_single(self, x):

        x = x.reshape(1, -1)

        return self.spe(x)[0]

    # =================================
    # Hotelling T²
    # =================================

    def t2(self, X):

        """
        Hotelling T²

        T² = t^T Λ⁻¹ t
        """

        X_norm = self.model.transform(X)

        T = np.dot(X_norm, self.model.components)

        lambda_k = self.eigenvalues

        T2 = np.sum((T ** 2) / lambda_k, axis=1)

        return T2

    # =================================
    # 单样本 T²
    # =================================

    def t2_single(self, x):

        x = x.reshape(1, -1)

        return self.t2(x)[0]

    # =================================
    # 同时计算 SPE 和 T²
    # =================================

    def score(self, X):

        spe = self.spe(X)

        t2 = self.t2(X)

        return spe, t2

    # =================================
    # 单样本评分
    # =================================

    def score_single(self, x):

        spe = self.spe_single(x)

        t2 = self.t2_single(x)

        return spe, t2
