# metric_model.py
import math
import random
from time_model import TimeSeriesModel
from config import Config

class MetricModel:
    def generate(self, t, event):
        cpu = TimeSeriesModel.multi_periodic(
            t, 0.0001, 0.000015, 0.00001, 0.000004,
            Config.DAY_PERIOD, Config.WEEK_PERIOD
        )

        response_time = TimeSeriesModel.multi_periodic(
            t, 0.2, 0.05, 0.03, 0.02,
            Config.DAY_PERIOD, Config.WEEK_PERIOD
        )

        memory = TimeSeriesModel.multi_periodic(
            t, 0.06, 0.02, 0.015, 0.01,
            Config.DAY_PERIOD, Config.WEEK_PERIOD
        )

        disk = TimeSeriesModel.multi_periodic(
            t, 0.15, 0.03, 0.02, 0.01,
            Config.DAY_PERIOD, Config.WEEK_PERIOD
        )

        io_read = TimeSeriesModel.multi_periodic(
            t, 30, 10, 8, 3,
            Config.DAY_PERIOD, Config.WEEK_PERIOD
        )

        io_write = TimeSeriesModel.multi_periodic(
            t, 15, 6, 5, 2,
            Config.DAY_PERIOD, Config.WEEK_PERIOD
        )

        service_rt = response_time * random.uniform(1.1, 1.3)
        service_qps = max(100, 900 - service_rt * 1000 + random.randint(-30, 30))

        # ========= 异常影响 =========
        if event:
            factor = 1 + 0.5 * math.sin(
                2 * math.pi * event.pos / event.length
            )

            if event.kind == "CPU_PRESSURE":
                cpu *= 3 * factor
                response_time *= 1.5 * factor
                service_rt *= 1.5 * factor

            elif event.kind == "SERVICE_LATENCY":
                response_time *= 2.5 * factor
                service_rt *= 2.8 * factor
                service_qps *= 0.6

            elif event.kind == "IO_BOTTLENECK":
                io_read *= 2.5 * factor
                io_write *= 2.5 * factor
                response_time *= 1.4 * factor

        return (
            cpu,
            response_time,
            memory,
            disk,
            io_read,
            io_write,
            service_rt,
            service_qps
        )
