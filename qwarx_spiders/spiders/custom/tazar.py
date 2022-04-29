from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "tazar"
    allowed_domains = ['tazar.nc']
    sitemap_urls = ["https://www.tazar.nc/sitemap_index.xml"]
