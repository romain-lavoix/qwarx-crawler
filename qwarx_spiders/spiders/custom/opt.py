from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "opt"
    allowed_domains = ['opt.nc']
    sitemap_urls = ["https://www.opt.nc/sitemap.xml"]
