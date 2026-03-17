from datetime import datetime


def str_to_ms(ts):

    ts = str(ts).strip()

    # UNIX时间戳
    if ts.isdigit():
        return int(ts) * 1000

    formats = [
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y-%m-%d %H:%M:%S"
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(ts, fmt)
            return int(dt.timestamp() * 1000)
        except ValueError:
            pass

    raise ValueError(ts)
