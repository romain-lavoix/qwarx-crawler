from ..base import BaseSpider
from ...utils.qwarx_crawl_spider import QwarxCrawlSpider


class Spider(QwarxCrawlSpider, BaseSpider):
    name = "lavisducagou"
    allowed_domains = ['lavisducagou.nc']
    start_urls = ['https://www.lavisducagou.nc']
