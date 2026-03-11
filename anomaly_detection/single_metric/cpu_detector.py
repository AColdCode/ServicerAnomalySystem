from anomaly_detection.single_metric.base_detector import BaseSingleMetricDetector


class CpuAnomalyDetector(BaseSingleMetricDetector):

    def __init__(self):

        super().__init__(
            metric_name="cpu_usage",
            period=288,
            z_threshold=3
        )