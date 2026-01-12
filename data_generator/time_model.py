# time_model.py
import math
import random

class TimeSeriesModel:
    @staticmethod
    def multi_periodic(
        t,
        base,
        day_amp,
        week_amp,
        noise,
        day_period,
        week_period
    ):
        value = (
            base
            + day_amp * math.sin(2 * math.pi * t / day_period)
            + week_amp * math.sin(2 * math.pi * t / week_period)
            + random.gauss(0, noise)
        )
        return max(0.0, value)
