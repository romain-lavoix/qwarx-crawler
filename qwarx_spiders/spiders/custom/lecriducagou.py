from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "lecriducagou"
    allowed_domains = ['lecriducagou.org']
    sitemap_urls = ["http://lecriducagou.org/sitemap_index.xml"]
