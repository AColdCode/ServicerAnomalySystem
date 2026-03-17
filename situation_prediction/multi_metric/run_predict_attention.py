import os

from data_source.db_reader import DBReader
from preprocessing.preprocessor import TimeSeriesPreprocessor

from situation_prediction.multi_metric.predictors.attention_predictor import AttentionPredictor
from situation_prediction.multi_metric.utils.result_saver import ResultSaver
from situation_prediction.multi_metric.config import *


def main():

    db = DBReader(DATA_PATH)

    preprocessor = TimeSeriesPreprocessor()

    predictor = AttentionPredictor()

    table = db.get_server_tables()[0]

    print("预测服务器:", table)

    df = db.read_server_metrics(table)

    df = preprocessor.process(df)

    df = preprocessor.normalize(df, FEATURE_COLUMNS)

    predictor.load_model(table)

    result = predictor.predict(df)

    result = preprocessor.inverse_normalize(
        result,
        [f"real_{c}" for c in FEATURE_COLUMNS] +
        [f"pred_{c}" for c in FEATURE_COLUMNS]
    )

    save_path = os.path.join(
        PREDICT_DIR,
        f"{table}_prediction.csv"
    )

    ResultSaver.save(
        result,
        save_path
    )


if __name__ == "__main__":

    main()
