import argparse
import time
from tasktimer.timer import Timer
from tasktimer.tempo import TempoReporter
import os
import click
import requests
from requests.auth import HTTPBasicAuth

def get_ticket_list(args):

    tickets = requests.post(
        "https://{}/rest/api/3/search".format(args.domain),
        json={
            "jql": 'status = "In Progress" AND assignee = currentUser() ORDER BY created DESC',
            "maxResults": 10,
            "fields": [
                "summary",
            ],
        },
        auth=HTTPBasicAuth(args.username, args.jira_token),
        headers={"accept": "application/json"}
    )
    if not tickets.ok:
        raise Exception(tickets.text)
    tickets = tickets.json()
    tickets = tickets.get('issues', [])

    choices = {}
    for i in tickets:
        choices[i['key']] = i['fields']['summary']
    return choices


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", default=os.environ.get("JIRA_DOMAIN"))
    parser.add_argument("--username", default=os.environ.get("JIRA_USERNAME"))
    parser.add_argument("--jira_token", default=os.environ.get("JIRA_TOKEN"))
    parser.add_argument("--tempo_token", default=os.environ.get("JIRA_TEMPO_TOKEN"))
    args = parser.parse_args()

    tickets = get_ticket_list(args)
    for t, txt in tickets.items():
        click.echo("{}: {}".format(t, txt))
    ticket_number = click.prompt("Choose a ticket",
                                 show_choices=False, type=click.Choice(tickets, case_sensitive=False))
    description = click.prompt("What are you doing now?")

    timer = Timer(ticket_number, description)
    with timer as t:
        while True:
            try:
                click.clear()
                click.echo(t)
                time.sleep(60)
            except KeyboardInterrupt:
                break

    click.echo("{}\n".format(timer))

    if click.confirm('Log to tempo?', default=True):
        # send to TEMPO
        domain = args.domain
        username = args.username
        jira_token = args.jira_token
        tempo_token = args.tempo_token
        if domain and username and tempo_token and jira_token:
            more_info = []
            while True:
                text = click.prompt('Add more info. (blank to end)', default="")
                if text:
                    more_info.append(text)
                else:
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
