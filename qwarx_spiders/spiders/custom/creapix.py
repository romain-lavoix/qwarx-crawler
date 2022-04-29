from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider
from ...utils.parse import parse


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "creapix"
    allowed_domains = ['creapix.nc']
    sitemap_urls = ["https://www.creapix.nc/sitemap.xml"]

    def image_f(self, response):
        return response.css('img').xpath('@src').extract()[0]

    def parse(self, response):
        return parse(self, response, image_f=self.image_f)
