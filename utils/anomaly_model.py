from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex


class AnomalyModel(QAbstractListModel):
    TimeRole = Qt.UserRole + 1
    ScoreRole = Qt.UserRole + 2
    IsAnomalyRole = Qt.UserRole + 3
    IsHandledRole = Qt.UserRole + 4
    TopMetricRole = Qt.UserRole + 5
    TimestampRole = Qt.UserRole + 6

    def __init__(self, data=None):
        super().__init__()
        self._data = data or []

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def data(self, index, role):
        if not index.isValid():
            return None

        item = self._data[index.row()]

        if role == self.TimeRole:
            return item.get("time", "")
        elif role == self.ScoreRole:
            return item.get("score", 0.0)
        elif role == self.IsAnomalyRole:
            return item.get("is_anomaly", 0)
        elif role == self.IsHandledRole:
            return item.get("is_handled", 0)
        elif role == self.TopMetricRole:
            return item.get("top_metric", "")
        elif role == self.TimestampRole:
            return item.get("timestamp", 0)

        return None

    def roleNames(self):
        return {
            self.TimeRole: b"time",
            self.ScoreRole: b"score",
            self.IsAnomalyRole: b"is_anomaly",
            self.IsHandledRole: b"is_handled",
            self.TopMetricRole: b"top_metric",
            self.TimestampRole: b"timestamp"
        }

    def setDataList(self, data_list):
        self.beginResetModel()
        self._data = data_list
        self.endResetModel()
