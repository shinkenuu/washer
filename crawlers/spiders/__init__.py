from scrapy import Spider

from models import Credential, Server

class WasherSpider(Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.server = Server.query.filter_by(name=WasherSpider.name).first()
        self.credential = next(self.server.all_credentials_available_to_vote)
