from qwarx_spiders.spiders.base import BaseSpider
from ...utils.qwarx_crawl_spider import QwarxCrawlSpider


class Spider(QwarxCrawlSpider, BaseSpider):
    name = "crawl_test"
    allowed_domains = ['trecodec.nc']
    start_urls = ['https://www.trecodec.nc/espace-pro/adhesion-et-eco-participation']
