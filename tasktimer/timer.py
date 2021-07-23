import datetime
import math


def _parse_s(s):
    out = []
    h = s / 60 // 60

    if h >= 1:
        s = s - h * 60 * 60
        out.append("{:.0f}h".format(h))

    m = s // 60

    if m >= 1 or h == 0:
        out.append("{:.0f}m".format(m))

    return " ".join(out)


class NotStarted(Exception):
    pass


class Timer(object):

    def __init__(self, description=None):
        self.description = description
        self.history = []
        self.first_start_time = None
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
        if self.total_time:
            return self.total_time.seconds
        else:
            return 0

    def start(self, now=None):
        if now is None:
            now = datetime.datetime.now()
        self.start_time = now

        if self.first_start_time is None:
            self.first_start_time = self.start_time

    def end(self, now=None):
        if self.start_time is None:
            raise NotStarted

        if now is None:
            now = datetime.datetime.now()
        self.history.append(now - self.start_time)
        self.total_time = datetime.timedelta(seconds=0)
        for i in self.history:
            self.total_time += i

        # reset
        self.start_time = None

        # minimum is 15 minutes
        seconds_by_15_min = math.ceil(self.total_time.seconds / 900) * 900
        self.total_time = datetime.timedelta(seconds=seconds_by_15_min)

    def print(self):
        return "{}".format(_parse_s(self.elapsed_s))
