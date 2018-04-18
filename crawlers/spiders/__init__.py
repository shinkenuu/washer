from scrapy import Spider

from database.models import Server


class WasherSpider(Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.server = Server.query.filter_by(name=self.name).first()

        if self.server is None:
            raise ValueError('Spider "{}" is not registered in the current database'.format(self.name))

        self.credential = self.server.next_credential_to_vote
