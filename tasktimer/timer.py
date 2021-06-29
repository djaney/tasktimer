import datetime
import time


def _parse_s(s):
    out = []
    h = s / 60 // 60

    if h >= 1:
        s = s - h * 60 * 60
        out.append("{}h".format(h))

    m = s // 60

    if m >= 1 or h == 0:
        out.append("{}m".format(m))

    return " ".join(out)


class Timer(object):

    def __init__(self, name):
        self.name = name
        self.start_time = datetime.datetime.now()
        self.total_time = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.total_time = datetime.datetime.now() - self.start_time

    def __str__(self):
        return self.print()

    @property
    def elapsed_s(self):
        end = self.total_time if self.total_time else datetime.datetime.now()
        return (end - self.start_time).seconds

    def print(self):
        return "{} - {}".format(_parse_s(self.elapsed_s), self.name)

