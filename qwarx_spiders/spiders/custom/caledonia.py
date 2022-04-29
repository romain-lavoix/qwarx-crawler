from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "caledonia"
    allowed_domains = ['caledonia.nc']
    sitemap_urls = ["https://www.caledonia.nc/sitemap.xml"]
