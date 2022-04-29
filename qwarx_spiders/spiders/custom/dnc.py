from ..base import BaseSpider
from ...utils.qwarx_crawl_spider import QwarxCrawlSpider


class Spider(QwarxCrawlSpider, BaseSpider):
    name = "dnc"
    allowed_domains = ['dnc.nc']
    start_urls = ['http://www.dnc.nc']

    def description_f(self, response):
        descriptions = response.xpath("//meta[@name='description']/@content").extract()
        if len(descriptions) == 1:
            return descriptions[0]
        else:
            return descriptions[1]

    def parse_item(self, response, **kwargs):
        return QwarxCrawlSpider.parse_item(self, response, description_f=self.description_f)
