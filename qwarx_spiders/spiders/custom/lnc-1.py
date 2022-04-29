from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "lnc-1"
    allowed_domains = ['lnc.nc']
    sitemap_urls = ["https://www.lnc.nc/sitemap.xml?page=1"]
    sitemap_rules = [('/article/(?!monde)', 'parse')]
