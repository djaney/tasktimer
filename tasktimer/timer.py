import datetime


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

    def __init__(self, ticket_number, description=None):
        self.ticket_number = ticket_number
        self.description = description
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
        if self.total_time:
            return self.total_time.seconds
        else:
            return (datetime.datetime.now() - self.start_time).seconds

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
        return "{} - {}".format(_parse_s(self.elapsed_s), self.ticket_number)
