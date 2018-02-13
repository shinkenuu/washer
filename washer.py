import json
from os.path import dirname, join, realpath

from scrapy.crawler import CrawlerProcess


from washer.spiders.destiny import MapleDestinySpider


if __name__ == '__main__':
    with open(join(dirname(realpath(__file__)), 'oracle.json'), 'r') as json_file:
        oracle = json.load(json_file)

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    spider_dict = {
        'MapleDestiny': MapleDestinySpider
    }

    for server in oracle['servers']:

        spider = spider_dict[server['name']]
        spider.crawl_spots = server['crawl_spots']

        for credential in server['credentials']:

            spider.username = credential['username']
            spider.password = credential['password']

            process.crawl(spider)
            process.start()
