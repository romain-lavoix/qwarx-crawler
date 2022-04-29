from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "province-sud"
    allowed_domains = ['province-sud.nc']
    sitemap_urls = ["https://www.province-sud.nc/sitemap.xml"]
