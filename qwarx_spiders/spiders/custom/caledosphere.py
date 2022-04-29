from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "caledosphere"
    allowed_domains = ['caledosphere.com']
    sitemap_urls = ["https://caledosphere.com/sitemap_index.xml"]
