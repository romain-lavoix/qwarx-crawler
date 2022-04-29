from ..base import BaseSpider
from ...utils.qwarx_crawl_spider import QwarxCrawlSpider


class Spider(QwarxCrawlSpider, BaseSpider):
    name = "quincaillerie-caledonienne"
    allowed_domains = ['quincaillerie-caledonienne.nc']
    start_urls = ['http://quincaillerie-caledonienne.nc']
