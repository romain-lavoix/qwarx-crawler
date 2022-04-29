from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "lemagdugouv"
    allowed_domains = ['lemagdugouv.nc']
    sitemap_urls = ["http://lemagdugouv.nc/sitemap_index.xml"]
