from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from ..base import BaseSpider
from ...utils.qwarx_crawl_spider import QwarxCrawlSpider


class Spider(QwarxCrawlSpider, BaseSpider):
    name = "oeil"
    allowed_domains = ['oeil.nc']
    start_urls = ['http://www.oeil.nc']

    rules = (
        Rule(LinkExtractor(
            unique=True,
            allow=(r'http://www.epokboutique.com/epokboutique/.+',),
            deny=(r'http://www.epokboutique.com/epokboutique/component/.+',)
        ),
            callback='parse_item',
            follow=True,
        ),
    )
