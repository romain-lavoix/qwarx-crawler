from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider
from ...utils.parse import parse


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "madein"
    allowed_domains = ['madein.nc']
    sitemap_urls = ["https://madein.nc/robots.txt"]

    def date_f(self, response):
        date = response.selector.xpath('//time/@pubdate').extract_first()
        return date

    def parse(self, response):
        return parse(self, response, date_f=self.date_f)