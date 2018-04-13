from datetime import datetime

from factory import SubFactory, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from models import Credential, Server
from database import db_session


class ServerFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Server
        sqlalchemy_session = db_session

    name = 'server_name'
    base_url = 'https://domain.com'


class CredentialFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Credential
        sqlalchemy_session = db_session

    username = Sequence(lambda n: 'username_' + str(n))
    password = 'secret'
    able_to_vote = False
    last_vote_datetime = datetime.utcnow()

    server = SubFactory(ServerFactory)
