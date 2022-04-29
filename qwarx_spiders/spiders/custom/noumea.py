from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "noumea"
    allowed_domains = ['noumea.nc']
    sitemap_urls = ["http://www.noumea.nc/sitemap.xml"]
