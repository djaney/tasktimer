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


class NotStarted(Exception):
    pass


class Timer(object):

    def __init__(self, name):
        self.name = name
        self.start_time = None
        self.total_time = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end()

    def __str__(self):
        return self.print()

    @property
    def elapsed_s(self):
        if self.start_time is None:
            return 0
        end = self.total_time if self.total_time else datetime.datetime.now()
        return (end - self.start_time).seconds

    def start(self, now=None):
        if now is None:
            now = datetime.datetime.now()
        self.start_time = now

    def end(self, now=None):
        if self.start_time is None:
            raise NotStarted

        if now is None:
            now = datetime.datetime.now()
        self.total_time = now - self.start_time

    def print(self):
        return "{} - {}".format(_parse_s(self.elapsed_s), self.name)
