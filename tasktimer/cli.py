import datetime
import argparse
import time
from tasktimer.timer import Timer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    args = parser.parse_args()
    with Timer(args.name) as t:
        while True:
            try:
                print(t)
                time.sleep(60)
            except KeyboardInterrupt:
                break
        print(t)
