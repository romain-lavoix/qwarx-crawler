from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "caledonie-ensemble"
    allowed_domains = ['caledonie-ensemble.com']
    sitemap_urls = ["https://caledonie-ensemble.com/robots.txt"]
