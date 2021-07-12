import argparse
import time
from tasktimer.timer import Timer
from tasktimer.tempo import TempoReporter
import os
import click


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ticket_number")
    parser.add_argument("description")
    parser.add_argument("--domain")
    parser.add_argument("--username")
    parser.add_argument("--jira_token")
    parser.add_argument("--tempo_token")
    args = parser.parse_args()
    timer = Timer(args.ticket_number, args.description)
    with timer as t:
        while True:
            try:
                click.clear()
                click.echo(t)
                time.sleep(60)
            except KeyboardInterrupt:
                break
    click.echo(timer)

    if click.confirm('Log to tempo?'):
        # send to TEMPO
        domain = args.domain if args.domain else os.environ.get("JIRA_DOMAIN")
        username = args.username if args.username else os.environ.get("JIRA_USERNAME")
        jira_token = args.jira_token if args.jira_token else os.environ.get("JIRA_TOKEN")
        tempo_token = args.tempo_token if args.tempo_token else os.environ.get("JIRA_TEMPO_TOKEN")
        if domain and username and tempo_token and jira_token:
            more_info = []
            while True:
                try:
                    text = click.prompt('Add more info. (Ctrl+C when done)')
                    more_info.append(text)
                except KeyboardInterrupt:
                    break

            timer.description += "\n\n{}".format("\n".join(more_info))

            click.echo("Sending...")
            reporter = TempoReporter(timer, domain, username, jira_token, tempo_token)
            res = reporter.send()
            click.echo("Sent!" if res.ok else "Failed")
        else:
            click.echo("There is something wrong with the configuration", err=True)


if __name__ == "__main__":
    main()
