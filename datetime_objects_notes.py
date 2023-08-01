from datetime import datetime, timezone


def wrong_usage():
    ts = 1571595618.0
    x = datetime.utcfromtimestamp(ts)
    x_ts = x.timestamp()

    assert ts == x_ts, f"{ts} != {x_ts}"


def right_usage():
    ts = 1571595618.0
    x = datetime.fromtimestamp(ts, tz=timezone.utc)
    x_ts = x.timestamp()

    assert ts == x_ts, f"{ts} != {x_ts}"  # This assertion succeeds


if __name__ == "__main__":
    right_usage()
