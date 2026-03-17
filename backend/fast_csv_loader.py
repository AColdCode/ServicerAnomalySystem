import csv

from .time_utils import str_to_ms


def parse_bool(v):

    if v is None:
        return 0

    s = str(v).strip().lower()

    if s in ("1", "true", "yes"):
        return 1

    return 0


def safe_float(v):

    try:
        return float(v)
    except:
        return 0.0


class FastCSVLoader:

    def load(self, path):

        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    # ------------------------------------------------
    # 单指标异常检测 cpu_usage_detect.csv
    # ------------------------------------------------

    def parse_single_detect(self, rows):

        data = []

        for r in rows:

            data.append(
                {
                    "ts": str_to_ms(r["timestamp"]),
                    "cpu": safe_float(r["cpu_usage"]),
                    "real": parse_bool(r["cpu_anomaly"]),
                    "detect": parse_bool(r["detect_anomaly"]),
                }
            )

        return data

    # ------------------------------------------------
    # PCA多指标异常检测 pca_detect.csv
    # ------------------------------------------------

    def parse_multi_detect(self, rows):

        data = []

        for r in rows:

            spe = safe_float(r.get("spe"))
            t2 = safe_float(r.get("t2"))

            data.append(
                {
                    "ts": str_to_ms(r["timestamp"]),

                    "cpu": safe_float(r["cpu_usage"]),
                    "resp": safe_float(r["response_time"]),
                    "mem": safe_float(r["memory_usage"]),
                    "disk": safe_float(r["disk_usage"]),

                    "real": parse_bool(r["is_anomaly"]),
                    "detect": parse_bool(r["anomaly"]),

                    "spe": spe,
                    "t2": t2,

                    "root": r.get("root_cause", "")
                }
            )

        return data

    # ------------------------------------------------
    # 单指标预测 cpu_prediction.csv
    # ------------------------------------------------

    def parse_single_predict(self, rows):

        data = []

        for r in rows:

            data.append(
                {
                    "ts": str_to_ms(r["timestamp"]),
                    "real": safe_float(r["real"]),
                    "pred": safe_float(r["pred"]),
                }
            )

        return data

    # ------------------------------------------------
    # LSTM多指标预测 lstm_prediction.csv
    # ------------------------------------------------

    def parse_multi_predict(self, rows):

        data = []

        for r in rows:

            data.append(
                {
                    "ts": str_to_ms(r["timestamp"]),

                    "real_cpu": safe_float(r["real_cpu_usage"]),
                    "real_resp": safe_float(r["real_response_time"]),
                    "real_mem": safe_float(r["real_memory_usage"]),
                    "real_disk": safe_float(r["real_disk_usage"]),

                    "pred_cpu": safe_float(r["pred_cpu_usage"]),
                    "pred_resp": safe_float(r["pred_response_time"]),
                    "pred_mem": safe_float(r["pred_memory_usage"]),
                    "pred_disk": safe_float(r["pred_disk_usage"]),
                }
            )

        return data
