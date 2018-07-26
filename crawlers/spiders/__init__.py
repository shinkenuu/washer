from scrapy import Spider

from models import Server


class WasherSpider(Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.server = Server.query.filter(name= self.name).one()
        self.credential = self.next_credential_to_vote()

    def next_credential_to_vote(self):
        return min(
            [credential for credential in self.server.credentials if credential.able_to_vote],
            key=lambda credential: credential.last_vote_datetime)
