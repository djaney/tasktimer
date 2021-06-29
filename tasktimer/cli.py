import argparse
import time
from tasktimer.timer import Timer
from tasktimer.tempo import TempoReporter
import os


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
    account_id = args.account_id if args.account_id else os.environ.get("JIRA_ACCOUNT_ID")
    token = args.token if args.token else os.environ.get("JIRA_TEMPO_TOKEN")
    if account_id and token:
        reporter = TempoReporter(timer, account_id.replace("-", ""), token)
        res = reporter.send()
        print(res.status_code, res.text)
