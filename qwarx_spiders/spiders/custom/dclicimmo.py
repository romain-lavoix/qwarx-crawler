from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider
from ...utils.parse import parse


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "dclicimmo"
    allowed_domains = ['dclicimmo.nc']
    sitemap_urls = ["http://dclicimmo.nc/robots.txt"]
    check_duplicates = True
    rotate_user_agent = True
    follow_canonical_links = True
    custom_settings = {
        'REDIRECT_ENABLED': 'True',
    }

    def parse(self, response):
        return parse(self, response)
