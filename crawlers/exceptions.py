class CrawlerException(Exception):
    def __init__(self, server_name, username, **kwargs):
        self.server_name = server_name
        self.username = username
        super().__init__(**kwargs)


class UnableToVote(CrawlerException):
    def __str__(self):
        return 'Unable to vote in server {} for username {}'.format(self.server_name, self.username)


class LoginFailed(CrawlerException):
    def __str__(self):
        return 'Unable to log in server {} with username {}'.format(self.server_name, self.username)


class VoteFailed(CrawlerException):
    def __str__(self):
        return 'Failed voting in server {} with username {}'.format(self.server_name, self.username)
