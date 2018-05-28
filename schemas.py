from datetime import datetime

class CredentialSchema(object):
    def __init__(self, **kwargs):
        self.username = kwargs['username']
        self.password =  kwargs['password']
        self.able_to_vote = kwargs['able_to_vote']
        self.last_vote_datetime = datetime.strptime(kwargs['last_vote_datetime'], '%Y-%m-%d %H:%M:%S')


class ServerSchema(object):
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.base_url = kwargs['base_url']
        self.credentials = [CredentialSchema(**credential_dict) for credential_dict in kwargs['credentials']]


class WasherSchema(object):
    def __init__(self, **kwargs):
        self.servers = [ServerSchema(**server_dict) for server_dict in kwargs['servers']]
