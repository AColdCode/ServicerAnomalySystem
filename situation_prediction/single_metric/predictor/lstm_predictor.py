import torch
import pandas as pd
import numpy as np


class LSTMPredictor:

    def __init__(self, model, batch_size=256):

        self.model = model
        self.batch_size = batch_size

    def predict(self, X, y, ts):

        self.model.eval()

        X = torch.tensor(X, dtype=torch.float32)

        preds = []

        with torch.no_grad():

            for i in range(0, len(X), self.batch_size):

                batch = X[i:i + self.batch_size]

                out = self.model(batch)

                preds.extend(out.numpy().flatten())

        preds = np.array(preds)

        result = pd.DataFrame({
            "timestamp": ts,
            "real": y,
            "pred": preds
        })

        return result
