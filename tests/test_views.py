from unittest import TestCase
import json

from app import app
from app.database import db_session
from tests.model_factories import CredentialFactory


class ViewTests(TestCase):
    def setUp(self):
        super().setUp()
        app.testing = True
        self.app = app.test_client()

    def test_server_name_not_found_error(self):
        response = self.app.get('/unexistent_server_name')

        self.assertEqual(response.status_code, 404)

        json_response = json.loads(response.data.decode('utf-8'))

        expected_response = {
            'error': 404,
            'text': 'Resource not found'
        }

        self.assertDictEqual(expected_response, json_response)

    # TODO mock scrapy call
    def test_success_response(self):
        server_name = 'server_name'

        next_to_vote_credential = CredentialFactory(server__name=server_name)
        db_session.flush()

        response = self.app.get('/' + server_name)
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(next_to_vote_credential.username, json_response['credential_that_voted']['username'])

    def test_view_is_calling_scrapy(self):
        raise NotImplemented
