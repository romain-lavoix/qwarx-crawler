from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "lnc-all"
    allowed_domains = ['lnc.nc']
    sitemap_urls = ["https://www.lnc.nc/sitemap.xml"]
    sitemap_rules = [('/article/(?!monde|france|pacifique)', 'parse')]
