from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "ludik"
    allowed_domains = ['ludik.nc']
    sitemap_urls = ["http://www.ludik.nc/robots.txt"]
