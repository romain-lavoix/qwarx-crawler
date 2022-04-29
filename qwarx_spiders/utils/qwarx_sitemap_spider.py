from scrapy.spiders import SitemapSpider

from .parse import parse


class QwarxSitemapSpider(SitemapSpider):
    check_duplicates = True
    rotate_user_agent = True
    follow_canonical_links = True
    custom_settings = {
        'REDIRECT_ENABLED': 'True',
    }

    def parse(self, response):
        return parse(self, response)
