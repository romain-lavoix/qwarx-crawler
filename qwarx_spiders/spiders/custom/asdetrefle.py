from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider
from ...utils.parse import parse


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "asdetrefle"
    allowed_domains = ['asdetrefle.nc']
    sitemap_urls = ["https://www.asdetrefle.nc/robots.txt"]


    def price_f(self, response):
        price = response.selector.xpath("//span[@class='price']/text()").extract_first()
        return price

    def parse(self, response):
        return parse(self, response, price_f=self.price_f)
