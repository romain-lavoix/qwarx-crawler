from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "ladepeche"
    allowed_domains = ['ladepeche.nc']
    sitemap_urls = ["https://ladepeche.nc/sitemap_index.xml"]
