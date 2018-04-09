import json
from unittest import TestCase

from mock import mock
from crawlers import Spider
from crawlers.crawler import CrawlerProcess

from app import app
from app.database import db_session
from tests.app.model_factories import CredentialFactory


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

    @mock.patch.object(CrawlerProcess, 'start')
    def test_success_response(self, mocked_start):
        server_name = 'server_name'

        next_to_vote_credential = CredentialFactory(server__name=server_name)
        db_session.flush()

        response = self.app.get('/' + server_name)
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(next_to_vote_credential.username, json_response['credential_that_voted']['username'])
        mocked_start.assert_called_once()

    @mock.patch('app.views.prepare_spider', return_value=Spider(name='mocked'))
    @mock.patch.object(CrawlerProcess, 'crawl')
    @mock.patch.object(CrawlerProcess, 'start')
    def test_view_is_calling_scrapy(self, mocked_start, mocked_crawl, mocked_prepare_spider):
        CredentialFactory(server__name='server_name')
        db_session.flush()

        self.app.get('/server_name')

        mocked_crawl.assert_called_once_with(mocked_prepare_spider.return_value)
        mocked_start.assert_called_once()
