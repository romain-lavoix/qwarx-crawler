from ..base import BaseSpider
from ...utils.qwarx_crawl_spider import QwarxCrawlSpider


class Spider(QwarxCrawlSpider, BaseSpider):
    name = "jeco"
    allowed_domains = ['jeco.nc']
    start_urls = ['https://jeco.nc']
