from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "meubles-import"
    allowed_domains = ['meubles-import.nc']
    sitemap_urls = ["http://meubles-import.nc/sitemap_index.xml"]
