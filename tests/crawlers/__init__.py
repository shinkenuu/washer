from os import path
from scrapy.http import TextResponse, Request


def create_spider_response(spider_name, html_filename, url=None):
    """
    Create a spider response based on arguments as tests fixtures
    :param spider_name: the spider owner of the desired response
    :param html_filename:
    :param url: url to use at the request
    :return:
    """
    with open(path.join('./tests/crawlers/', spider_name, 'assets', html_filename), 'r') as html_file:
        html_content = html_file.read()

    url = url or 'http://domain.com/'

    request = Request(url=url)

    response = TextResponse(url=url, request=request, body=html_content, encoding='utf-8')

    return response
