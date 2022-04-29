from ..base import BaseSpider
from ...utils.qwarx_crawl_spider import QwarxCrawlSpider


class Spider(QwarxCrawlSpider, BaseSpider):
    name = "mademoisellel"
    allowed_domains = ['mademoisellel.nc']
    start_urls = ['http://www.mademoisellel.nc']
