import torch
import os
from torch.utils.data import DataLoader, TensorDataset

from situation_prediction.multi_metric.models.attention_lstm import AttentionLSTM
from situation_prediction.multi_metric.datasets.sequence_dataset import SequenceDataset
from situation_prediction.multi_metric.utils.model_manager import ModelManager
from situation_prediction.multi_metric.config import *


class AttentionTrainer:

    def __init__(self):

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        print("训练设备:", self.device)

        self.model = AttentionLSTM(
            INPUT_SIZE,
            HIDDEN_SIZE,
            NUM_LAYERS,
            PRED_LENGTH
        ).to(self.device)

        self.criterion = torch.nn.MSELoss()

        self.optimizer = torch.optim.Adam(
            self.model.parameters(),
            lr=LR
        )

        self.dataset_builder = SequenceDataset(
            SEQ_LENGTH,
            PRED_LENGTH
        )

    def prepare_data(self, df):

        data = df[FEATURE_COLUMNS].values

        X, Y = self.dataset_builder.create_sequences(data)

        X = torch.tensor(X, dtype=torch.float32)

        Y = torch.tensor(Y, dtype=torch.float32)

        return X, Y

    def train_epoch(self, loader):

        self.model.train()

        total_loss = 0

        for x, y in loader:

            x = x.to(self.device)

            y = y.to(self.device)

            self.optimizer.zero_grad()

            pred, _ = self.model(x)

            loss = self.criterion(pred, y)

            loss.backward()

            self.optimizer.step()

            total_loss += loss.item()

        return total_loss / len(loader)

    def train(self, df, server_name):

        X, Y = self.prepare_data(df)

        loader = DataLoader(
            TensorDataset(X, Y),
            batch_size=BATCH_SIZE,
            shuffle=True
        )

        for epoch in range(EPOCHS):

            loss = self.train_epoch(loader)

            print(f"{server_name} Epoch {epoch+1} / {EPOCHS} Loss={loss:.6f}")

        model_path = os.path.join(
            MODEL_DIR,
            f"{server_name}_attention_lstm.pth"
        )

        ModelManager.save(self.model, model_path)

        print("模型保存:", model_path)
