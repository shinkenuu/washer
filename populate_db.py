import json

from models import *


json_content = json.load(open('./servers_and_credentials.json'))

server_data = json_content['servers'][0]
credentials_data = server_data.pop('credentials')

server = Server(**server_data)

session.add(server)
session.commit()

for credential_data in credentials_data:
    session.add(Credential(**credential_data, server=server))

session.commit()
