from datetime import datetime
import json


class Schema(object):
    attributes = []

    def __init__(self, **kwargs):
        for attr in self.attributes:
            self.__setattr__(attr, kwargs[attr])

    def __iter__(self):
        """
        Create a formatted ```self``` to a dict with only the attributes of the Schema
        """
        for attr in self.attributes:
            key = attr
            value = self.__getattribute__(attr)

            if isinstance(value, Schema):
                yield key, dict(value)
                continue

            yield key, value


class CredentialSchema(Schema):
    attributes = ['username', 'password', 'able_to_vote', 'last_vote_datetime']

    def __init__(self, **kwargs):
        super(Schema, self).__init__()

        self.last_vote_datetime = datetime.strptime(kwargs['last_vote_datetime'], '%Y-%m-%d %H:%M:%S')


class ServerSchema(Schema):
    attributes = ['name', 'base_url', 'credentials']

    def __init__(self, **kwargs):
        super(Schema, self).__init__()

        self.credentials = [CredentialSchema(**credential_dict) for credential_dict in kwargs['credentials']]


class WasherSchema(Schema):
    attributes = ['servers']

    def __init__(self, **kwargs):
        super(Schema, self).__init__()

        self.servers = [ServerSchema(**server_dict) for server_dict in kwargs['servers']]
