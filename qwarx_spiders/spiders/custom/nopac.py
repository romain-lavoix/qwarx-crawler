from ..base import BaseSpider
from ...utils.qwarx_crawl_spider import QwarxCrawlSpider


class Spider(QwarxCrawlSpider, BaseSpider):
    name = "nopac"
    allowed_domains = ['nopac.nc']
    start_urls = ['https://nopac.nc']
