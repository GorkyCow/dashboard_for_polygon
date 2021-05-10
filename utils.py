from collections import OrderedDict
from datetime import datetime, timedelta


def ts_to_datetime(ts) -> str:
    return datetime.fromtimestamp(ts / 1000.0).strftime("%Y-%m-%d %H:%M:00")


def get_last_n_days(day=None, n=30):
    if day:
        end = datetime.strptime(day, "%Y-%m-%d")
    else:
        end = datetime.now()
    start = end - timedelta(n)
    return list(
        OrderedDict(
            ((start + timedelta(_)).strftime("%Y-%m-%d"), None)
            for _ in range((end - start).days)
        ).keys()
    )


def day_to_range(day):
    return f"{day} 00:00:00", f"{day} 23:59:59"


def get_next_day_str(day):
    return (datetime.strptime(day, "%Y-%m-%d") + timedelta(1)).strftime("%Y-%m-%d")
