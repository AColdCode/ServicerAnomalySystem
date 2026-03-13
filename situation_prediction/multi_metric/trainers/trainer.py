import os
import torch
import numpy as np
import pandas as pd
from torch.utils.data import DataLoader, TensorDataset

from situation_prediction.multi_metric.models.lstm_predictor import MultiMetricLSTM
from situation_prediction.multi_metric.datasets.sequence_dataset import SequenceDataset
from situation_prediction.multi_metric.utils.model_manager import ModelManager
from situation_prediction.multi_metric.config import *


class MultiMetricTrainer:
    """
    多指标态势预测训练器
    """

    def __init__(self):

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        print("使用设备:", self.device)

        # 构建模型
        self.model = MultiMetricLSTM(
            input_size=INPUT_SIZE,
            hidden_size=HIDDEN_SIZE,
            num_layers=NUM_LAYERS,
            pred_len=PRED_LENGTH
        ).to(self.device)

        # 损失函数
        self.criterion = torch.nn.MSELoss()

        # 优化器
        self.optimizer = torch.optim.Adam(
            self.model.parameters(),
            lr=LR
        )

        # 序列生成器
        self.dataset_builder = SequenceDataset(
            SEQ_LENGTH,
            PRED_LENGTH
        )

    # =========================================================
    # DataFrame -> Tensor
    # =========================================================
    def _prepare_data(self, df):

        data = df[FEATURE_COLUMNS].values

        X, Y = self.dataset_builder.create_sequences(data)

        X = torch.tensor(X, dtype=torch.float32)

        Y = torch.tensor(Y, dtype=torch.float32)

        return X, Y

    # =========================================================
    # DataLoader
    # =========================================================
    def _create_loader(self, X, Y):

        dataset = TensorDataset(X, Y)

        loader = DataLoader(
            dataset,
            batch_size=BATCH_SIZE,
            shuffle=True
        )

        return loader

    # =========================================================
    # 单轮训练
    # =========================================================
    def _train_one_epoch(self, loader):

        self.model.train()

        total_loss = 0

        for batch_x, batch_y in loader:

            batch_x = batch_x.to(self.device)

            batch_y = batch_y.to(self.device)

            self.optimizer.zero_grad()

            pred = self.model(batch_x)

            loss = self.criterion(pred, batch_y)

            loss.backward()

            self.optimizer.step()

            total_loss += loss.item()

        return total_loss / len(loader)

    # =========================================================
    # 训练单服务器
    # =========================================================
    def train_single_server(self, df, server_name):

        print("开始训练:", server_name)

        X, Y = self._prepare_data(df)

        loader = self._create_loader(X, Y)

        for epoch in range(EPOCHS):

            loss = self._train_one_epoch(loader)

            print(f"{server_name} Epoch {epoch+1}/{EPOCHS} Loss={loss:.6f}")

        model_path = os.path.join(MODEL_DIR, f"{server_name}_lstm.pth")

        ModelManager.save(self.model, model_path)

        print("模型保存:", model_path)

    # =========================================================
    # 批量训练
    # =========================================================
    def train_batch_servers(self, server_dfs):

        """
        server_dfs:

        [
            ("server_01_metrics", df),
            ("server_02_metrics", df)
        ]
        """
        for server_name, df in server_dfs:

            self.train_single_server(df, server_name)

        print("批次训练完成")

    # =========================================================
    # 合并训练 (多服务器联合)
    # =========================================================
    def train_multi_servers(self, server_dfs):

        """
        将多个服务器数据合并训练
        """

        all_X = []
        all_Y = []

        for server_name, df in server_dfs:

            print("准备数据:", server_name)

            X, Y = self._prepare_data(df)

            all_X.append(X)

            all_Y.append(Y)

        X = torch.cat(all_X)

        Y = torch.cat(all_Y)

        print("训练样本数:", len(X))

        loader = self._create_loader(X, Y)

        for epoch in range(EPOCHS):

            loss = self._train_one_epoch(loader)

            print(f"Epoch {epoch+1}/{EPOCHS} Loss={loss:.6f}")

        model_path = os.path.join(MODEL_DIR, "global_lstm_model.pth")

        ModelManager.save(self.model, model_path)

        print("全局模型保存:", model_path)
