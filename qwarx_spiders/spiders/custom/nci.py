from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "nci"
    allowed_domains = ['nci.nc']
    sitemap_urls = ["https://nci.nc/sitemap_index.xml"]
