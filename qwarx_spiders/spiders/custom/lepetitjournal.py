from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider
from ...utils.parse import parse


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "lepetitjournal"
    allowed_domains = ['lepetitjournal.com']
    sitemap_urls = ["https://lepetitjournal.com/sitemap.xml"]

    sitemap_rules = [('/nouvelle-caledonie/', 'parse')]
    custom_settings = {
        'REDIRECT_ENABLED': 'True',
    }

    def date_f(self, response):
        lines = response.xpath('//div/text()').extract()
        date = None
        for line in lines:
            if 'Mis à jour le' in line:
                parsed_line = line[line.index('Mis à jour le') + 14:line.index('Mis à jour le') + 24]
                date = '{}-{}-{}'.format(parsed_line[6:], parsed_line[3:5], parsed_line[:2])
        return date

    def parse(self, response):
        return parse(self, response, date_f=self.date_f)
