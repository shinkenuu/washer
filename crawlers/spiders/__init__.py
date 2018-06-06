import json

from scrapy import Spider

from schemas import WasherSchema


class WasherSpider(Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        json_data_read = self.read_from_json()
        self.json_data = WasherSchema(**json_data_read)

        self.server = next((server for server in self.json_data.servers if server.name == self.name), None)
        self.credential = self.next_credential_to_vote()

    def read_from_json(self, json_file_path='servers_and_credentials.json'):
        with open(json_file_path, 'r') as json_file:
            return json.load(json_file)

    def write_to_json(self, json_file_path='servers_and_credentials.json'):
        with open(json_file_path, 'w') as json_file:
            return json.dump(dict(self.json_data), json_file)

    def next_credential_to_vote(self):
        return min(
            [credential for credential in self.server.credentials if credential.able_to_vote],
            key=lambda credential: credential.last_vote_datetime)
