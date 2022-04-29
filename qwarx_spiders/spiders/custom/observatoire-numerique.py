from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "observatoire-numerique"
    allowed_domains = ['observatoire-numerique.nc']
    sitemap_urls = ["https://observatoire-numerique.nc/sitemap_index.xml"]
