import requests
from requests.auth import HTTPBasicAuth


class TempoReporter(object):
    def __init__(self, timer, domain, username, jira_token, tempo_token):
        self.timer = timer
        self.domain = domain
        self.username = username
        self.jira_token = jira_token
        self.tempo_token = tempo_token

    def send(self, ticket_number, description):
        res = requests.get(
            "https://{}/rest/api/3/myself".format(self.domain),
            auth=HTTPBasicAuth(self.username, self.jira_token),
            headers={"accept": "application/json"}
        )
        profile = res.json()
        return requests.post(
            'https://api.tempo.io/core/3/worklogs',
            json={
                "issueKey": ticket_number,
                "timeSpentSeconds": self.timer.elapsed_s,
                "startDate": self.timer.first_start_time.date().strftime("%Y-%m-%d"),
                "startTime": self.timer.first_start_time.time().strftime("%H:%M:%S"),
                "description": description,
                "authorAccountId": profile.get("accountId"),
            },
            headers={
                "Authorization": "Bearer {}".format(self.tempo_token)
            }
        )
