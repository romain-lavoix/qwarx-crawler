from ..base import BaseSpider
from ...utils.qwarx_crawl_spider import QwarxCrawlSpider


class Spider(QwarxCrawlSpider, BaseSpider):
    name = "ncpresse"
    allowed_domains = ['ncpresse.nc']
    start_urls = ['https://www.ncpresse.nc']
