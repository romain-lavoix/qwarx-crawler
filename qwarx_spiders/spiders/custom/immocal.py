import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from ..base import BaseSpider
from ...utils.qwarx_crawl_spider import QwarxCrawlSpider


class Spider(QwarxCrawlSpider, BaseSpider):
    name = "immocal"
    allowed_domains = ['immocal.nc']
    start_urls = []
    rules = (
        Rule(LinkExtractor(
            unique=True,
            allow=(
                r'https://www.immocal.nc/bien/.+/'
            ),
        ),
            callback='parse_item',
            follow=True,
        ),
    )

    def generate_start_urls(self):
        yield 'https://www.immocal.nc/a-louer/'
        yield 'https://www.immocal.nc/a-vendre/'
        yield 'https://www.immocal.nc/promotion/'

        for i in range(2, 50):
            yield 'https://www.immocal.nc/a-louer/page/{}/'.format(i)
            yield 'https://www.immocal.nc/a-vendre/page/{}/'.format(i)

    def start_requests(self):
        for url in self.generate_start_urls():
            yield scrapy.Request(url, dont_filter=True)

    def description_f(self, response):
        return response.xpath('//p/text()').extract()[:5]

    def price_f(self, response):
        return response.css('.prix').xpath('text()').extract()[0]

    def real_estate_type_f(self, response):
        type = response.css('.status').xpath('text()').extract()[0]

        if 'vendre' in type:
            type = 'Vente'
        if 'louer' in type:
            type = 'Location'

        return type

    def image_f(self, response):
        return response.css('img').xpath('@src').extract()[1]

    def parse_item(self, response, **kwargs):
        return QwarxCrawlSpider.parse_item(self, response, description_f=self.description_f, image_f=self.image_f, price_f=self.price_f,
                                           real_estate_type_f=self.real_estate_type_f)
