from copy import deepcopy
from datetime import datetime
from unittest import TestCase

from app.database import db_session
from tests.model_factories import CrawlFormFactory, CredentialFactory, ServerFactory


class ServerTests(TestCase):
    def test_property_next_to_vote(self):
        server = ServerFactory()

        next_to_vote_cred = CredentialFactory(username='user1', server=server,
                                              last_vote_datetime=datetime(2017, 1, 1))
        unable_to_vote_cred = CredentialFactory(username='user2', server=server, able_to_vote=False,
                                                last_vote_datetime=datetime(2017, 1, 1))
        latest_to_vote_cred = CredentialFactory(username='user3', server=server,
                                                last_vote_datetime=datetime(2018, 1, 1))

        db_session.flush()

        self.assertEqual(server.next_to_vote, next_to_vote_cred)


class CrawlFormTests(TestCase):
    def test_interpretation(self):
        form = CrawlFormFactory(
            name='__server__.name', # Just to test multiple dynamic keys
            data={
                     'username': '__credential__.username'
            },
            xpath='//__any_key__',
        )

        server = ServerFactory()
        credential = CredentialFactory()

        interpreted_form = form.interpret(credential=credential, server=server)

        expected_form = deepcopy(form)

        expected_form.name = server.name
        expected_form.data = {'username': credential.username},
        expected_form.xpath = '//__any_key__'

        self.assertEqual(expected_form, interpreted_form)


    def test_property_to_scrapy_form(self):
        scrapy_form_args = ['formname', 'formxpath', 'formcss', 'formnumber', 'formdata', 'clickdata', 'dontlick']

        form = CrawlFormFactory()

        parsed_form = form.to_scrapy_form

        for key in parsed_form.keys():
            self.assertIn(key, scrapy_form_args)
