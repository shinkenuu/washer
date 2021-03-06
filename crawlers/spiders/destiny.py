from datetime import datetime
import logging

from scrapy import FormRequest, Request

from crawlers.spiders import WasherSpider
from crawlers.exceptions import LoginFailed, UnableToVote, VoteFailed


class DestinySpider(WasherSpider):
    name = 'destiny'

    @staticmethod
    def is_logged_in(response):
        """
        Check if there is any user logged in.
        :param response:
        :return: `True` if logged, `False` otherwise.
        """
        if response.xpath('//a[@class="btn btn-info dropdown-toggle"]'):
            return True
        return False

    @staticmethod
    def can_vote(response):
        """
        Check if any vote button is enabled.
        :param response:
        :return: `True` if able to vote, `False` otherwise.
        """
        if response.xpath('//input[@class="btn btn-large btn-block btn-primary "]'):
            return True
        return False

    def start_requests(self):
        yield Request(url='{}/login/'.format(self.server.host), callback=self.login)

    def login(self, response):
        """
        Login with the credentials provided at instantiation
        :param response: the /login page response
        :return: a FormRequest with the credentials to login, calling `login_callback`
        """
        form_kwargs = {
            'formxpath': '//form[@class="form-signin"]',
            'formdata': {'username': self.credential.username, 'password': self.credential.password},
            'clickdata': {'type': 'submit'}
        }

        return FormRequest.from_response(response, callback=self.login_callback, **form_kwargs)

    def login_callback(self, response):
        if not self.is_logged_in(response):
            raise LoginFailed(server_name=self.server.name, username=self.credential.username)

        return Request(url='{}/vote/'.format(self.server.host), callback=self.vote)

    def vote(self, response):
        """
        Vote for `credential` on all available sites
        :param response: the /vote page response
        :return: a generator with a FormRequest for each available vote form
        """
        if not self.can_vote(response):
            raise UnableToVote(server_name=self.server.name, username=self.credential.username)

        if response.xpath('//input[@value="Vote on Gtop100 (6k NX)"]'):
            form_kwarg = {
                'formnumber': 0,
                'clickdata': {'value': 'Vote on Gtop100 (6k NX)'}
            }

            return FormRequest.from_response(response, callback=self.vote_callback, **form_kwarg)

        raise VoteFailed(server_name=self.server.name, username=self.credential.username)

    def vote_callback(self, response):
        if response.status == 200 and self.server.host not in response.url:
            logging.info('Vote successful for username {} at {}'.format(self.credential.username, self.server.name))

            self.record_voting(self.credential, datetime.utcnow())

            return

        raise VoteFailed(server_name=self.server.name, username=self.credential.username)
