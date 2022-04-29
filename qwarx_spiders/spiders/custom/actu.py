from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "actu"
    allowed_domains = ['actu.nc']
    sitemap_urls = ["https://www.actu.nc/sitemap_index.xml"]
