from datetime import datetime

from scrapy.crawler import CrawlerProcess

from app.database import db_session
from app.models import Server

from crawlers.spiders.destiny import DestinySpider
from crawlers.exceptions import LoginFailed, UnableToVote


SPIDERS = {
    'destiny': DestinySpider
}


def crawl(server: Server):
    spider_type = SPIDERS[server.name]

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    crawl_results = {
        'credential_that_vote': None,
        'errors': []
    }

    for credential in server.all_credentials_available_to_vote:
        spider = spider_type(
            credential={
                'username': credential.username,
                'password': credential.password,
            },
            urls={
                'login': server.base_url + '/login',
                'vote': server.base_url + '/vote'
            }
        )

        try:
            process.crawl(spider)
            process.start()

        except LoginFailed as ex:
            credential.able_to_vote = False
            crawl_results['errors'].append(str(ex))
            continue

        except UnableToVote as ex:
            credential.last_vote_datetime = datetime.utcnow()
            crawl_results['errors'].append(str(ex))
            continue

        credential.last_vote_datetime = datetime.utcnow()
        crawl_results['credential_that_vote'] = credential.serialize()
        break

    db_session.commit()
    return crawl_results
