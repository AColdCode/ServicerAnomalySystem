import math
from collections import defaultdict


class TrendProcessor:
    def generate_trend(self, timestamps, values, anomalies, range_type="1h"):

        bucket_map = {
            "1h": 300,
            "6h": 600,
            "1d": 1800,
            "7d": 7200
        }

        bucket = bucket_map.get(range_type, 5)

        _, final, _ = self.aggregate(timestamps, values, anomalies, bucket)

        return final

    def aggregate(self, timestamps, values, anomalies, bucket_size):
        buckets = defaultdict(list)

        for ts, val, an in zip(timestamps, values, anomalies):
            bucket = int(ts // bucket_size) * bucket_size
            buckets[bucket].append((val, an))

        new_ts = []
        new_vals = []
        new_anomalies = []

        prev_val = None

        for b in sorted(buckets.keys()):
            items = buckets[b]

            vals = [v for v, _ in items]
            ans = [a for _, a in items]

            max_v = max(vals)
            min_v = min(vals)

            if prev_val is None:
                chosen_val = max_v
            else:
                if max_v > prev_val:
                    chosen_val = max_v
                else:
                    chosen_val = min_v

            chosen_anomaly = 1 if any(ans) else 0

            new_ts.append(b)
            new_vals.append(chosen_val)
            new_anomalies.append(chosen_anomaly)

            prev_val = chosen_val

        return new_ts, new_vals, new_anomalies

    def predictAggregate(self, timestamps, values, bucket_size):
        from collections import defaultdict

        buckets = defaultdict(list)

        for ts, val in zip(timestamps, values):
            bucket = int(ts // bucket_size) * bucket_size
            buckets[bucket].append(val)

        new_ts = []
        new_vals = []

        prev_val = None

        for b in sorted(buckets.keys()):
            vals = buckets[b]

            max_v = max(vals)
            min_v = min(vals)

            if prev_val is None:
                chosen_val = max_v
            else:
                if max_v > prev_val:
                    chosen_val = max_v
                else:
                    chosen_val = min_v

            new_ts.append(b)
            new_vals.append(chosen_val)

            prev_val = chosen_val

        return new_ts, new_vals
