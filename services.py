from datetime import datetime

from scrapy.crawler import CrawlerProcess

from database import db_session
from models import Server

from crawlers.spiders.destiny import DestinySpider
from crawlers.exceptions import LoginFailed, UnableToVote


def prepare_spider():
    credential = next(credential in server.all_credentials_available_to_vote)
    spider = spider_type(

    )
