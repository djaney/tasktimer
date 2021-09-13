import requests
from requests.auth import HTTPBasicAuth


class Tempo(object):
    def __init__(self, domain, username, jira_token, tempo_token):
        self.domain = domain
        self.username = username
        self.jira_token = jira_token
        self.tempo_token = tempo_token

    def send_worklogs(self, timer, ticket_number, description):
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
                "timeSpentSeconds": timer.elapsed_s,
                "startDate": timer.first_start_time.date().strftime("%Y-%m-%d"),
                "startTime": timer.first_start_time.time().strftime("%H:%M:%S"),
                "description": description,
                "authorAccountId": profile.get("accountId"),
            },
            headers={
                "Authorization": "Bearer {}".format(self.tempo_token)
            }
        )

    def get_in_progress_tickets(self):
        tickets = requests.post(
            "https://{}/rest/api/3/search".format(self.domain),
            json={
                "jql": 'status = "In Progress" AND assignee = currentUser() ORDER BY created DESC',
                "maxResults": 10,
                "fields": [
                    "summary",
                ],
            },
            auth=HTTPBasicAuth(self.username, self.jira_token),
            headers={"accept": "application/json"}
        )
        if not tickets.ok:
            raise Exception(tickets.text)
        tickets = tickets.json()
        tickets = tickets.get('issues', [])

        output = {}
        for i in tickets:
            output[i['key']] = i['fields']['summary']
        return output
