from datetime import datetime

from scrapy import Spider

from models import Credential, Server, session


class WasherSpider(Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.server = session.query(Server).filter_by(name=self.name).one()
        self.credential = self.next_credential_to_vote()

    def next_credential_to_vote(self):
        return min(
            [credential for credential in self.server.credentials if credential.able_to_vote],
            key=lambda credential: credential.last_vote_datetime)

    def record_voting(self, credential: Credential, vote_datetime: datetime):
        credential.last_vote_datetime = vote_datetime
        session.add(credential)
        session.commit()
