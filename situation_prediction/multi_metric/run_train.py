import math
from data_source.db_reader import DBReader
from preprocessing.preprocessor import TimeSeriesPreprocessor

from situation_prediction.multi_metric.trainers.trainer import MultiMetricTrainer
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

    print("开始多指标态势预测模型训练")

    db = DBReader(DATA_PATH)

    preprocessor = TimeSeriesPreprocessor()

    trainer = MultiMetricTrainer()

    table = db.get_server_tables()[0]

    print("读取数据:", table)

    df = db.read_server_metrics(table)

    df = preprocessor.process(df)

    df = preprocessor.normalize(df, FEATURE_COLUMNS)

    trainer.train_single_server(df, table)

    print("\n训练完成")


if __name__ == "__main__":

    main()
