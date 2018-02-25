from scrapy import FormRequest, Spider, Request


class WasherSpider(Spider):
    name = 'washer'

    def __init__(self, urls: dict, forms: dict, **kwargs):
        self.urls = urls
        self.forms = forms

        super().__init__(**kwargs)

    def start_requests(self):
        yield Request(url=self.urls['login'], callback=self.parse_login)

    def login_callback(self, response):
        if response.status == 200 and self.forms['login'][0]['username'] in response.text:
            print('Login successful')
            return Request(url=self.urls['vote'], callback=self.parse_vote)

        raise Exception('Login failed')

    def parse_login(self, response):
        for form in self.forms['login']:
            yield FormRequest.from_response(response, callback=self.login_callback, **form)

    def vote_callback(self, response):
        if response.status == 200:
            print('Vote successful')
            return

        raise Exception('Vote failed')

    def parse_vote(self, response):
        for form in self.forms['vote']:
            yield FormRequest.from_response(response, callback=self.vote_callback, **form)
