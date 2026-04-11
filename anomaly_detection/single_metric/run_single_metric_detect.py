from anomaly_detection.single_metric.single_metric_service import SingleMetricDetectionService

if __name__ == "__main__":

    DB_PATH = "../../data_generator/metrics.db"
    TABLE_NAME = "server_01_metrics"

    metrics = [
        "cpu_usage", "response_time", "memory_usage", "disk_usage", "io_read", "io_write", "service_rt", "service_qps"
    ]

    for metric in metrics:

        service = SingleMetricDetectionService(
            DB_PATH,
            TABLE_NAME,
            metric
        )

        service.run()
