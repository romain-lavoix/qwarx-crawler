from ..base import BaseSpider
from ...utils.qwarx_crawl_spider import QwarxCrawlSpider


class Spider(QwarxCrawlSpider, BaseSpider):
    name = "mont-dore"
    allowed_domains = ['mont-dore.nc']
    start_urls = ['https://www.mont-dore.nc']
