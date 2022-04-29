from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "gouv"
    allowed_domains = ['gouv.nc']
    sitemap_urls = ["https://gouv.nc/sitemap.xml"]
