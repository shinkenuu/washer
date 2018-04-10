import json
from unittest import TestCase

from mock import mock

from app import app
from app.database import db_session
from crawlers.exceptions import LoginFailed, UnableToVote
from tests.app.model_factories import CredentialFactory, ServerFactory


class ViewTests(TestCase):
    def setUp(self):
        super().setUp()

        # create temp db

        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        super().tearDown()

        # destroy temp db

    def test_server_name_not_found_error(self):
        response = self.app.get('/unexistent_server_name')

        self.assertEqual(response.status_code, 404)

        json_response = json.loads(response.data.decode('utf-8'))

        expected_response = {
            'error': 404,
            'text': 'Resource not found'
        }

        self.assertDictEqual(expected_response, json_response)

    @mock.patch('app.views.crawl')
    def test_response(self, mocked_crawl):
        server = ServerFactory()

        credential_that_voted = CredentialFactory(server=server)
        credential_with_failed_login = CredentialFactory(server=server)
        credential_unable_to_vote = CredentialFactory(server=server)

        mocked_crawl.return_value = {
            'credential_that_voted': credential_that_voted.serialize(),
            'errors': [
                LoginFailed(server_name=server.name, username=credential_with_failed_login.username).__str__(),
                UnableToVote(server_name=server.name, username=credential_unable_to_vote.username).__str__(),
            ]
        }

        response = self.app.get('/' + server.name)
        self.assertEqual(response.status_code, 500)

        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(mocked_crawl.return_value, json_response)

    @mock.patch('app.views.crawl', return_value={})
    def test_view_is_calling_crawl(self, mocked_crawl):
        server = ServerFactory()

        self.app.get('/' + server.name)

        mocked_crawl.assert_called_once()
