from scrapy import FormRequest, Spider, Request

from crawlers.exceptions import LoginFailed, UnableToVote


class WasherSpider(Spider):
    name = 'washer'

    def __init__(self, credential: dict, urls: dict, **kwargs):
        if {'username', 'password'} > set(credential.keys()):
            raise ValueError('Invalid credentials dict')

        if {'login', 'vote'} > set(urls.keys()):
            raise ValueError('Invalid urls dict')

        self.credential = credential
        self.urls = urls

        super().__init__(**kwargs)

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
        yield Request(url=self.urls['login'], callback=self.login)

    def login(self, response):
        """
        Login with the credentials provided at instantiation
        :param response: the /login page response
        :return: a FormRequest with the credentials to login, calling `login_callback`
        """
        form_kwargs = {
            'formxpath': '//form[@class="form-signin"]',
            'formdata': self.credential,
            'clickdata': {'type': 'submit'}
        }

        return FormRequest.from_response(response, callback=self.login_callback, **form_kwargs)

    def login_callback(self, response):
        if not self.is_logged_in(response):
            raise LoginFailed(server='destiny', username=self.credential['username'])

        return Request(url=self.urls['vote'], callback=self.vote)

    def vote(self, response):
        """
        Vote for `credential` on all available sites
        :param response: the /vote page response
        :return: a generator with a FormRequest for each available vote form
        """
        if not self.can_vote(response):
            raise UnableToVote(server='destiny', username=self.credential['username'])

        forms_kwargs = []

        if response.xpath('//input[@value="Vote on Gtop100 (4k NX)"]'):
            forms_kwargs.append(
                {
                    'formnumber': 0,
                    'clickdata': {'value': 'Vote on Gtop100 (4k NX)'}
                }
            )

        if response.xpath('//input[@value="Vote on UltimatePS (2k NX)"]'):
            forms_kwargs.append(
                {
                    'formnumber': 1,
                    'clickdata': {'value': 'Vote on UltimatePS (2k NX)'}
                }
            )

        for form_kwargs in forms_kwargs:
            yield FormRequest.from_response(response, callback=self.vote_callback, **form_kwargs)

    def vote_callback(self, response):
        if response.status == 200:
            print('Vote successful')
            return

        raise Exception('Vote failed')
