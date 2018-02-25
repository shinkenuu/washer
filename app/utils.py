from app.models import Credential, Server

from scrapy import Spider

def prepare_spider(spider_class: type(Spider), server: Server, credential: Credential):
    spots = sorted([_ for _ in server.crawl_spots], key=lambda spot: spot.order_of_crawling)

    forms = {}
    urls = {}

    for spot in spots:
        forms[spot.id] = [form.to_scrapy_form(server=server, credential=credential) for form in spot.forms]
        urls[spot.id] = spot.url

    return spider_class(urls=urls, forms=forms)
