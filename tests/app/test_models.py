from datetime import datetime

from freezegun import freeze_time

from app.database import db_session
from tests.app.model_factories import CredentialFactory, ServerFactory


def test_property_all_able_to_vote_credentials(self):
    server = ServerFactory()

    next_to_vote_cred = CredentialFactory(server=server, able_to_vote=True)
    unable_to_vote_cred = CredentialFactory(server=server, able_to_vote=False)
    last_to_vote_cred = CredentialFactory(server=server, able_to_vote=True, last_vote_datetime=datetime(year=2016))

    db_session.flush()

    self.assertEqual(set(server.all_able_to_vote_credentials), {next_to_vote_cred, last_to_vote_cred})


@freeze_time('2018-01-01')
def test_property_all_credentials_available_to_vote(self):
    server = ServerFactory()

    unable_to_vote = CredentialFactory(server=server, able_to_vote=False)
    latest_to_vote = CredentialFactory(server=server, able_to_vote=True, last_vote_datetime=datetime.utcnow())
    first_to_vote = CredentialFactory(server=server, able_to_vote=True,
                                      last_vote_datetime=datetime(year=2017, month=1, day=1))
    second_to_vote = CredentialFactory(server=server, able_to_vote=True,
                                       last_vote_datetime=datetime(year=2017, month=2, day=1))
    third_to_vote = CredentialFactory(server=server, able_to_vote=True,
                                      last_vote_datetime=datetime(year=2017, month=3, day=1))

    db_session.flush()
    self.assertEqual(server.all_credentials_available_to_vote, [first_to_vote, second_to_vote, third_to_vote])
