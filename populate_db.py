from datetime import datetime

from database import db_session
from models import Credential, Server


COMMON_CREDENTIAL_KWARGS = {
    'able_to_vote': True,
    'last_vote_datetime': datetime(year=2018, month=3, day=2)
}


DESTINY_SERVER = Server(name='destiny', base_url='http://mapledestiny.net')

DESTINY_CREDENTIALS = [
    Credential(username='8balls', password='ehnoiscarai', server=DESTINY_SERVER, **COMMON_CREDENTIAL_KWARGS),
    Credential(username='8balls2', password='ehnoiscarai', server=DESTINY_SERVER, **COMMON_CREDENTIAL_KWARGS),
    Credential(username='8balls3', password='ehnoiscarai', server=DESTINY_SERVER, **COMMON_CREDENTIAL_KWARGS),
    Credential(username='8balls4', password='ehnoiscarai', server=DESTINY_SERVER, **COMMON_CREDENTIAL_KWARGS),
    Credential(username='Matrim', password='5hadow', server=DESTINY_SERVER, **COMMON_CREDENTIAL_KWARGS),
    Credential(username='Vincent_', password='5hadow', server=DESTINY_SERVER, **COMMON_CREDENTIAL_KWARGS),
]


def insert_destiny_into_db():
    db_session.add_all([DESTINY_SERVER] + DESTINY_CREDENTIALS)
    db_session.commit()
