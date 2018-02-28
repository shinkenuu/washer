from unittest import TestCase

from app.database import db_session
from app.utils import prepare_spider
from crawlers.crawlers.spiders.destiny import WasherSpider
from tests.app.model_factories import CredentialFactory, CrawlFormFactory, CrawlSpotFactory, ServerFactory


class UtilsTests(TestCase):
    def test_prepare_spider(self):
        server = ServerFactory()

        spot_0 = CrawlSpotFactory(order_of_crawling=0, server=server)
        spot_1 = CrawlSpotFactory(order_of_crawling=1, server=server)

        spot_0_forms = [CrawlFormFactory(formid=0, spot=spot_0)]
        spot_1_forms = [CrawlFormFactory(formid=id, spot=spot_1) for id in range(2)]

        credential = CredentialFactory(server=server)

        db_session.flush()

        urls = {
            spot_0.id: spot_0.url,
            spot_1.id: spot_1.url,
        }

        forms = {
            spot_0.id: [form.to_scrapy_form(server=server,credential=credential) for form in spot_0_forms],
            spot_1.id: [form.to_scrapy_form(server=server,credential=credential) for form in spot_1_forms],
        }

        prepared_spider = prepare_spider(WasherSpider, server=server, credential=credential)

        expected_spider = WasherSpider(urls=urls, forms=forms)

        self.assertEqual(prepared_spider.urls, expected_spider.urls)
        self.assertEqual(prepared_spider.forms, expected_spider.forms)
