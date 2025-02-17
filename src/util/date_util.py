from datetime import datetime


def get_datetime():
    return datetime.now()


def get_timestamp(to_millis: bool = True):
    ts = get_datetime().timestamp()
    if to_millis:
        ts = int(ts * 1000)
    return ts


def from_millis(millis: int):
    return datetime.fromtimestamp(millis / 1000)
