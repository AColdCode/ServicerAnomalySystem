import math
from collections import defaultdict


class TrendProcessor:

    # =========================
    # 1. 分桶聚合（同时处理异常）
    # =========================
    def aggregate_with_anomaly(self, timestamps, values, anomalies, bucket_size):
        buckets = defaultdict(list)
        anomaly_buckets = defaultdict(int)

        for ts, val, an in zip(timestamps, values, anomalies):
            bucket = int(ts // bucket_size) * bucket_size
            buckets[bucket].append(val)
            if an == 1:
                anomaly_buckets[bucket] = 1

        sorted_keys = sorted(buckets.keys())

        aggregated = []
        aggregated_anomaly = []

        for k in sorted_keys:
            avg = sum(buckets[k]) / len(buckets[k])
            aggregated.append(avg)
            aggregated_anomaly.append(anomaly_buckets[k])

        return aggregated, aggregated_anomaly

    # =========================
    # 2. 指数平滑
    # =========================
    def exponential_smoothing(self, data, alpha=0.2):
        if not data:
            return []

        result = [data[0]]
        for i in range(1, len(data)):
            val = alpha * data[i] + (1 - alpha) * result[-1]
            result.append(val)

        return result

    # =========================
    # 3. 限制突变（防止尖刺）
    # =========================
    def clamp(self, data, threshold=0.3):
        if not data:
            return []

        result = [data[0]]
        for i in range(1, len(data)):
            diff = data[i] - result[-1]

            if abs(diff) > threshold:
                diff = threshold if diff > 0 else -threshold

            result.append(result[-1] + diff)

        return result

    def enhance_anomaly(self, smooth, aggregated, anomalies, strength=1.5, radius=2):
        """
        smooth: 平滑后的趋势
        aggregated: 原始分桶值（未平滑）
        anomalies: 0/1
        """
        n = len(smooth)
        enhanced = smooth[:]

        for i in range(n):
            if anomalies[i] == 1:
                # 👉 用“原始值 - 平滑值”作为异常强度
                delta = aggregated[i] - smooth[i]

                for j in range(-radius, radius + 1):
                    idx = i + j
                    if 0 <= idx < n:
                        weight = 1 - abs(j) / (radius + 1)
                        enhanced[idx] += delta * strength * weight

        return enhanced

    # =========================
    # 5. 压缩点数（防卡 UI）
    # =========================
    def downsample(self, data, max_points=100):
        if len(data) <= max_points:
            return data

        step = len(data) / max_points
        sampled = []
        i = 0

        while int(i) < len(data):
            sampled.append(data[int(i)])
            i += step

        return sampled

    # =========================
    # 6. 主流程（最终接口）
    # =========================
    def generate_trend(self, timestamps, values, anomalies, range_type="1h"):

        bucket_map = {
            "1h": 5,
            "6h": 30,
            "1d": 300,
            "7d": 3600
        }

        bucket = bucket_map.get(range_type, 5)

        aggregated, aggregated_anomaly = self.aggregate_with_anomaly(
            timestamps, values, anomalies, bucket
        )

        smooth = self.exponential_smoothing(aggregated, alpha=0.2)

        enhanced = self.enhance_anomaly(
            smooth,
            aggregated,
            aggregated_anomaly,
            strength=1.5,
            radius=2
        )

        final = self.downsample(enhanced, max_points=100)

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
