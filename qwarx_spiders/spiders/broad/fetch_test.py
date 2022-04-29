from scrapy import Request
from scrapy.spiders import Spider

from ...utils.parse import parse


class QuotesSpider(Spider):
    name = "fetch_test"
    check_duplicates = True
    rotate_user_agent = True
    custom_settings = {
        'REDIRECT_ENABLED': 'True',
        'DOWNLOAD_TIMEOUT': 60,
        'RETRY_ENABLED': 'True'

    }

    def start_requests(self):
        start_urls = ['https://caledosphere.com/']

        for url in start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        return parse(self, response)
