from ..base import BaseSpider
from scrapy.spiders import Spider
from scrapy import Request
from ...utils.parse import parse


class MySpider(Spider, BaseSpider):
    name = "lnc-rss"
    start_urls = ["http://feeds.feedburner.com/LesNouvellesCaledoniennes"]

    custom_settings = {
        'DELTAFETCH_ENABLED': False,
        'DOTSCRAPY_ENABLED': False
    }

    def parse(self, response):
        elements = response.xpath('//link/text()').extract()
        urls = elements[2:len(elements)]
        urls = list(filter(lambda url: '/monde/' not in url and '/france/' not in url and '/pacifique/' not in url, urls))
        for url in urls:
            yield Request(url=url, callback=self.parse_rss)

    def parse_rss(self, response):
        return parse(self, response)