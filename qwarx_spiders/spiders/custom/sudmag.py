from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "sudmag"
    allowed_domains = ['sudmag.nc']
    sitemap_urls = ["https://sudmag.nc/post-sitemap.xml"]
