import argparse
import time
from tasktimer.timer import Timer
from tasktimer.tempo import TempoReporter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ticket_number")
    parser.add_argument("description")
    parser.add_argument("--account_id")
    parser.add_argument("--token")
    args = parser.parse_args()
    timer = Timer(args.ticket_number, args.description)
    with timer as t:
        while True:
            try:
                print(t)
                time.sleep(60)
            except KeyboardInterrupt:
                break
    print(timer)

    # send to TEMPO
    if args.account_id and args.token:
        reporter = TempoReporter(timer, args.account_id, args.token)
        res = reporter.send()
        print(res.status_code, res.text)
