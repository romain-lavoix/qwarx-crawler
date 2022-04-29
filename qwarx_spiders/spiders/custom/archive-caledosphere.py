from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "archives-caledosphere"
    allowed_domains = ['archives.caledosphere.com']
    sitemap_urls = ["https://archives.caledosphere.com/sitemap_index.xml"]
