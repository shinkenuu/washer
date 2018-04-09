class UnableToVote(Exception):
    def __init__(self, server, username, **kwargs):
        self.server = server
        self.username = username

        super().__init__(**kwargs)

    def __str__(self):
        return 'Unable to vote in server {} for username {}'.format(self.server, self.username)


class LoginFailed(Exception):
    def __init__(self, server, username, **kwargs):
        self.server = server
        self.username = username

        super().__init__(**kwargs)

    def __str__(self):
        return 'Login failed in server {} for username {}'.format(self.server, self.username)
