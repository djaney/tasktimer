import argparse
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
    parser.add_argument("--ticket")
    parser.add_argument("--description")
    parser.add_argument("--domain", default=os.environ.get("JIRA_DOMAIN"))
    parser.add_argument("--username", default=os.environ.get("JIRA_USERNAME"))
    parser.add_argument("--jira_token", default=os.environ.get("JIRA_TOKEN"))
    parser.add_argument("--tempo_token", default=os.environ.get("JIRA_TEMPO_TOKEN"))
    args = parser.parse_args()

    if args.ticket:
        ticket_number = args.ticket
    else:
        tickets = get_ticket_list(args)
        for t, txt in tickets.items():
            click.echo("{}: {}".format(t, txt))
        ticket_number = click.prompt("Choose a ticket",
                                     show_choices=False, type=click.Choice(tickets, case_sensitive=False))
    if args.description:
        description = args.description
    else:
        description = click.prompt("What are you doing now?")

    timer = Timer()
    while True:
        with timer as t:
            click.clear()
            click.echo("Current time - {}".format(str(t)))
            while not click.confirm(click.style('STARTED, Pause now?', bg='green', fg='white'), default=True):
                pass
        click.clear()
        click.echo("Current time - {}".format(str(t)))
        if click.confirm(click.style('PAUSED, Stop now?', bg='red', fg='white'), default=False):
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

            description += "\n\n{}".format("\n".join(more_info))

            click.echo("Ticket: {}".format(ticket_number))
            click.echo("Description: {}".format(description))
            click.echo("Sending...")
            reporter = TempoReporter(timer, domain, username, jira_token, tempo_token)
            res = reporter.send(ticket_number, description)
            if res.ok:
                click.echo("Sent!")
            else:
                click.echo("Failed! {}".format(res.text), err=True)
        else:
            click.echo("There is something wrong with the configuration", err=True)


if __name__ == "__main__":
    main()
