import json

from scrapy import Spider

from schemas import WasherSchema


class WasherSpider(Spider):
    def __init__(self, json_schema_filepath=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.json_schema_filepath = json_schema_filepath or './servers_and_credentials.json'

        json_read = self.read_dict_from_json()
        self.schema = WasherSchema(**json_read)

        self.server = next((server for server in self.schema.servers if server.name == self.name), None)
        self.credential = self.next_credential_to_vote()

    def read_dict_from_json(self):
        with open(self.json_schema_filepath, 'r') as json_file:
            return json.load(json_file)

    def write_dict_to_json(self, content: dict):
        with open(self.json_schema_filepath, 'w') as json_file:
            return json.dump(content, json_file, indent=4, sort_keys=True)

    def next_credential_to_vote(self):
        return min(
            [credential for credential in self.server.credentials if credential.able_to_vote],
            key=lambda credential: credential.last_vote_datetime)
