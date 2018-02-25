from flask import abort, jsonify
from scrapy.crawler import CrawlerProcess

from app import app
from app.models import Server
from app.utils import prepare_spider
from crawlers.crawlers.spiders.destiny import WasherSpider


@app.route('/<server_name>', methods=['GET'])
def vote(server_name):
    server = Server.query.filter_by(name=server_name).first()

    if not server:
        abort(404)

    credential_to_vote = server.next_to_vote

    response = {
        'credential_that_voted': dict(credential_to_vote)
    }

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    spider = prepare_spider(spider_class=WasherSpider, server=server, credential=credential_to_vote)

    process.crawl(spider)
    process.start()

    return jsonify(response), 200
