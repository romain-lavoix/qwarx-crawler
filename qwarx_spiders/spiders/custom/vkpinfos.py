from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "vkpinfos"
    allowed_domains = ['vkpinfos.nc']
    sitemap_urls = ["https://www.vkpinfos.nc/sitemap.xml"]
