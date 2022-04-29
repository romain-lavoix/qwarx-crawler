from ..base import BaseSpider
from ...utils.qwarx_crawl_spider import QwarxCrawlSpider
from ...utils.parse import parse


class Spider(QwarxCrawlSpider, BaseSpider):
    name = "grossiste"
    allowed_domains = ['grossiste.nc']
    start_urls = ['http://grossiste.nc']

    def image_f(self, response):
        img = response.css('img').xpath('@src').extract()[0]
        return img

    def parse_item(self, response):
        return parse(self, response, image_f=self.image_f)
