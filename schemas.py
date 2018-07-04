from abc import ABC, abstractmethod

from utils import datetime_to_json_datetime, json_datetime_to_datetime

class Schema(ABC):
    @abstractmethod
    def to_dict(self):
        """
        Create a dict with data equivalent to the Schema.

        Used to store data into JSON files.
        """
        return {}

    def __iter__(self):
        self_dict = self.to_dict()
        for key, value in self_dict.items():
            yield key, value


class CredentialSchema(Schema):
    def __init__(self, username, password, able_to_vote, last_vote_datetime):
        self.username = username
        self.password = password
        self.able_to_vote = able_to_vote
        self.last_vote_datetime = json_datetime_to_datetime(last_vote_datetime)

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'able_to_vote': self.able_to_vote,
            'last_vote_datetime': datetime_to_json_datetime(self.last_vote_datetime)
        }


class ServerSchema(Schema):
    def __init__(self, name, base_url, credentials):
        self.name = name
        self.base_url = base_url
        self.credentials = [CredentialSchema(**credential) for credential in credentials]

    def to_dict(self):
        return {
            'name': self.name,
            'base_url': self.base_url,
            'credentials': [credential.to_dict() for credential in self.credentials]
        }


class WasherSchema(Schema):
    def __init__(self, servers):
        self.servers = [ServerSchema(**server) for server in servers]

    def to_dict(self):
        return {
            'servers': [server.to_dict() for server in self.servers]
        }
