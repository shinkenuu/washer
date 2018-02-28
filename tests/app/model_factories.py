from factory import SubFactory, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from app.database import db_session
from app.models import CrawlForm, CrawlSpot, Credential, Server


class ServerFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Server
        sqlalchemy_session = db_session

    name = 'server_name'


class CredentialFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Credential
        sqlalchemy_session = db_session

    username = Sequence(lambda n: 'username_' + str(n))
    password = 'secret'

    server = SubFactory(ServerFactory)


class CrawlSpotFactory(SQLAlchemyModelFactory):
    class Meta:
        model = CrawlSpot
        sqlalchemy_session = db_session

    order_of_crawling = Sequence(lambda n: n)
    url = 'http://numse.iu/q'

    server = SubFactory(ServerFactory)


class CrawlFormFactory(SQLAlchemyModelFactory):
    class Meta:
        model = CrawlForm
        sqlalchemy_session = db_session

    formid = '0'
    name = 'form_name'
    xpath = '//element[@attr="value"]'
    number = 0
    data = {'form_key': 'form_value'}
    click_data = {'click_key': 'click_value'}

    spot = SubFactory(CrawlSpotFactory)
