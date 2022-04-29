from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from ..base import BaseSpider
from ...utils.qwarx_crawl_spider import QwarxCrawlSpider


class Spider(QwarxCrawlSpider, BaseSpider):
    name = "ambitionreussite"
    allowed_domains = ['ambitionreussite.nc']
    start_urls = ['http://ambitionreussite.nc/ncatalogue']
    rules = (
        Rule(LinkExtractor(
            unique=True,
            allow=(
                r'http://ambitionreussite.nc/ncatalogue'
            )
        ),
            callback='parse_item',
            follow=True,
        ),
    )
