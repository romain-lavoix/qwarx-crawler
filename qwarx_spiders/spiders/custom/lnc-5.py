from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "lnc-5"
    allowed_domains = ['lnc.nc']
    sitemap_urls = ["https://www.lnc.nc/sitemap.xml?page=5"]
    sitemap_rules = [('/article/', 'parse')]
