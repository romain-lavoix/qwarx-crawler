import re

import tldextract
from scrapy import Request
from scrapy.spiders import Spider

from ..base import BaseSpider
from ...services.gsheet import GoogleDriveSheet
from ...utils.parse import get_domain
from ...utils.parse import parse

custom_cache_extract = tldextract.TLDExtract(cache_file='/resources/tldcache')


class HomePageSpider(Spider, BaseSpider, GoogleDriveSheet):
    name = "homepages"

    start_urls = ["https://www.domaine.nc/whos?who=A*"]

    custom_settings = {
        'REDIRECT_ENABLED': True,
        'DOWNLOAD_TIMEOUT': 60,
        'RETRY_ENABLED': True
    }

    def parse(self, response):

        elements = response.xpath('//td/a/text()').extract()
        domains = set(filter(lambda domain: re.compile(".*\.nc").match(domain), elements))

        # let's sync the gsheet db with the new domains
        self.update_nc_domains(domains)

        for row in self.get_sheet_rows('DOMAINS_EXT'):
            domains.add(row[0])

        urls = list(map(lambda d: "http://{}".format(d), domains)) + list(
            map(lambda d: "http://www.{}".format(d), domains))

        for url in urls:
            yield Request(url=url, callback=self.parse_homepage, meta={'deltafetch_key': get_domain(url)})

            if self.is_test_mode:
                break

    def parse_homepage(self, response):
        return parse(self, response, homepage=True)
