from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from ..base import BaseSpider
from ...utils.qwarx_crawl_spider import QwarxCrawlSpider


class Spider(QwarxCrawlSpider, BaseSpider):
    name = "easycourses"
    allowed_domains = ['easycourses.nc']
    start_urls = ['https://www.easycourses.nc/fr/']
    rules = (
        Rule(LinkExtractor(
            unique=True,
            allow=(
                r'https://www.easycourses.nc/fr/.+/.+',
            ),
        ),
            callback='parse_item',
            follow=True,
        ),
    )
