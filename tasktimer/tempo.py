import requests


class TempoReporter(object):
    def __init__(self, timer, account_id, token):
        self.timer = timer
        self.account_id = account_id
        self.token = token

    def send(self):
        return requests.post(
            'https://api.tempo.io/core/3/worklogs',
            data={
                "issueKey": self.timer.ticket_number,
                "timeSpentSeconds": self.timer.elapsed_s,
                "startDate": self.timer.start_time.date().strftime("%Y-%m-%d"),
                "startTime": self.timer.start_time.time().strftime("%H:%M:%S"),
                "description": self.timer.description,
                "authorAccountId": self.account_id,
            },
            headers={
                "Authorization": "Bearer {}".format(self.token)
            }
        )
