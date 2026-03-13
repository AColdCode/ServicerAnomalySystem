import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset


class LSTMTrainer:

    def __init__(self, model, lr=0.001, epochs=20, batch_size=64):

        self.model = model
        self.lr = lr
        self.epochs = epochs
        self.batch_size = batch_size

        self.criterion = nn.MSELoss()

        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)

    def train(self, X, y):

        X = torch.tensor(X, dtype=torch.float32)
        y = torch.tensor(y, dtype=torch.float32).view(-1, 1)

        dataset = TensorDataset(X, y)

        loader = DataLoader(
            dataset,
            batch_size=self.batch_size,
            shuffle=True
        )

        for epoch in range(self.epochs):

            total_loss = 0

            for batch_x, batch_y in loader:

                self.optimizer.zero_grad()

                outputs = self.model(batch_x)

                loss = self.criterion(outputs, batch_y)

                loss.backward()

                self.optimizer.step()

                total_loss += loss.item()

            avg_loss = total_loss / len(loader)

            print(f"Epoch {epoch+1}/{self.epochs}  Loss={avg_loss:.6f}")
