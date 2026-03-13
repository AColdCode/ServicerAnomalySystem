import pandas as pd
import os


class ResultSaver:

    @staticmethod
    def save(df, path):

        os.makedirs(os.path.dirname(path), exist_ok=True)

        df.to_csv(path, index=False)

        print("预测结果保存:", path)
        