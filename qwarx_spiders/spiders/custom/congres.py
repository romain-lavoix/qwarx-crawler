from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "congres"
    allowed_domains = ['congres.nc']
    sitemap_urls = ["http://www.congres.nc/sitemap_index.xml"]
