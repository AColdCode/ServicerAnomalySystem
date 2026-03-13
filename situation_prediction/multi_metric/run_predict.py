import os
import math

from data_source.db_reader import DBReader
from preprocessing.preprocessor import TimeSeriesPreprocessor

from situation_prediction.multi_metric.predictors.predictor import MultiMetricPredictor
from situation_prediction.multi_metric.utils.result_saver import ResultSaver
from situation_prediction.multi_metric.config import *


def split_batches(data, batch_size):

    batches = []

    total = len(data)

    num_batches = math.ceil(total / batch_size)

    for i in range(num_batches):

        start = i * batch_size

        end = start + batch_size

        batches.append(data[start:end])

    return batches


def main():

    print("开始多指标态势预测")

    db = DBReader(DATA_PATH)

    preprocessor = TimeSeriesPreprocessor()

    predictor = MultiMetricPredictor()

    table = db.get_server_tables()[0]

    print("\n处理服务器:", table)

    df = db.read_server_metrics(table)

    df = preprocessor.process(df)

    df = preprocessor.normalize(df, FEATURE_COLUMNS)

    predictor.load_model(table)

    result_df = predictor.predict_dataframe(df)

    result_df = preprocessor.inverse_normalize(
        result_df,
        [f"real_{c}" for c in FEATURE_COLUMNS] +
        [f"pred_{c}" for c in FEATURE_COLUMNS]
    )

    save_path = os.path.join(
        PREDICT_DIR,
        f"{table}_prediction.csv"
    )

    ResultSaver.save(result_df, save_path)

    print("\n预测完成")


if __name__ == "__main__":

    main()
