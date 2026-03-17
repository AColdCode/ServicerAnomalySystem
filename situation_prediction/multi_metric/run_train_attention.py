from data_source.db_reader import DBReader
from preprocessing.preprocessor import TimeSeriesPreprocessor

from situation_prediction.multi_metric.trainers.attention_trainer import AttentionTrainer
from situation_prediction.multi_metric.config import *


def main():

    db = DBReader(DATA_PATH)

    preprocessor = TimeSeriesPreprocessor()

    trainer = AttentionTrainer()

    table = db.get_server_tables()[0]

    df = db.read_server_metrics(table)

    df = preprocessor.process(df)

    df = preprocessor.normalize(df, FEATURE_COLUMNS)

    trainer.train(df, table)


if __name__ == "__main__":

    main()
