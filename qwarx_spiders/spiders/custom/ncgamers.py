from ..base import BaseSpider
from ...utils.qwarx_crawl_spider import QwarxCrawlSpider


class Spider(QwarxCrawlSpider, BaseSpider):
    name = "ncgamers"
    allowed_domains = ['ncgamers.nc']
    start_urls = ['http://ncgamers.nc']
