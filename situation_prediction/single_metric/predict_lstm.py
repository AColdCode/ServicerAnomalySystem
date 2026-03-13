from data_source.db_reader import DBReader
from preprocessing.preprocessor import TimeSeriesPreprocessor

from situation_prediction.single_metric.dataset.sequence_builder import SequenceBuilder
from situation_prediction.single_metric.models.lstm_model import LSTMModel
from situation_prediction.single_metric.predictor.lstm_predictor import LSTMPredictor
from situation_prediction.single_metric.utils.model_manager import ModelManager
from situation_prediction.single_metric.utils.result_saver import ResultSaver


def main():

    reader = DBReader("../../data_generator/metrics.db")

    table = reader.get_server_tables()[0]

    df = reader.read_server_metrics(table)

    processor = TimeSeriesPreprocessor()

    df = processor.process(df)

    series = df["cpu_usage"]

    series.index = df["timestamp"]

    builder = SequenceBuilder(window_size=30)

    X, y, ts = builder.build(series)

    model = LSTMModel()

    manager = ModelManager()

    model = manager.load(model, "cpu_lstm_model")

    predictor = LSTMPredictor(model)

    result = predictor.predict(X, y, ts)

    saver = ResultSaver()

    saver.save(result, "cpu_lstm_prediction.csv")


if __name__ == "__main__":

    main()
