from datetime import datetime


class Schema(object):
    fields = []

    def __init__(self, **kwargs):
        for field in self.fields:
            setattr(self, field, kwargs[field])

    def __iter__(self):
        for field in self.fields:
            key = field
            value = getattr(self, field)

            if isinstance(value, Schema):
                yield key, dict(value)
                continue

            yield key, value


class CredentialSchema(Schema):
    fields = ['username', 'password', 'able_to_vote', 'last_vote_datetime']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_vote_datetime = datetime.strptime(kwargs['last_vote_datetime'], '%Y-%m-%d %H:%M:%S')


class ServerSchema(Schema):
    fields = ['name', 'base_url', 'credentials']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        credentials_schemas = []
        for credential in self.credentials:
            credentials_schemas.append(CredentialSchema(**credential))

        self.credentials = credentials_schemas


class WasherSchema(Schema):
    fields = ['servers']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        servers_schemas = []
        for server in self.servers:
            servers_schemas.append(ServerSchema(**server))

        self.servers = servers_schemas
