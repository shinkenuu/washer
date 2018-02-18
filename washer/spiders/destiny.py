from scrapy import FormRequest, Spider, Request


class WasherSpider(Spider):
    name = 'washer'

    username = ''
    password = ''

    crawl_spots = {}

    def start_requests(self):
        yield Request(
            url=WasherSpider.crawl_spots['login'],
            callback=self.parse_login
        )

    def login_callback(self, response):
        if response.status == 200 and WasherSpider.username in response.text:
            print('Login successful')

            return Request(
                url=WasherSpider.crawl_spots['vote'],
                callback=self.parse_vote
            )

        raise Exception('Login failed')

    def parse_login(self, response):
        return FormRequest.from_response(
            response,
            formxpath='//form[@class="form-signin"]',
            formdata={
                'username': WasherSpider.username,
                'password': WasherSpider.password
            },
            clickdata={
                'type': 'submit'
            },
            callback=self.login_callback
        )

    def vote_callback(self, response):
        if response.status == 200 and WasherSpider.name not in response.url:
            print('Vote successful')
            return

        raise Exception('Vote failed')

    def parse_vote(self, response):
        click_datas = [
            {
                'value': 'Vote on Gtop100 (4k NX)'
            },
            {
                'value': 'Vote on UltimatePS (2k NX)'
            },
        ]

        for number, click_data in enumerate(click_datas):
            yield FormRequest.from_response(
                response,
                formnumber= number,
                clickdata=click_data,
                callback=self.vote_callback)
