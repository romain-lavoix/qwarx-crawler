from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "radiococotier"
    allowed_domains = ['radiococotier.nc']
    sitemap_urls = ["https://radiococotier.nc/sitemap.xml"]
