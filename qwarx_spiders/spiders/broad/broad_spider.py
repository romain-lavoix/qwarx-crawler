import scrapy

from ..base import BaseSpider
from ...services.algolia import AlgoliaSearchBase
from ...utils.qwarx_crawl_spider import QwarxCrawlSpider
from ...services.gsheet import GoogleDriveSheet
import json


class BroadSpider(QwarxCrawlSpider, AlgoliaSearchBase, BaseSpider, GoogleDriveSheet):
    name = 'broad_spider'

    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BroadSpider, cls).from_crawler(crawler, *args, **kwargs)
        domains_infos = spider.gsheet_get_domains_infos()

        spider.urls = []
        spider.allowed_domains = []
        extra_banned = ['wordpress.com', 'hatch.com', 'unblog.fr', 'ovh.co.uk', 'anfr.fr', 'jimdo.com', 'ird.fr',
                        'nautisme-nc.com', 'wikipedia.org']
        # For the broad spider to work, we need to run homepage crawl at least once first
        for url in spider.get_algolia_index().browse_all(
                {"filters": 'boost.homepage=1 AND NOT category:facebook AND NOT category:wikipedia'}):
            domain = url['id']['domain']
            spider.allowed_domains.append(domain)
            activated = False
            if domain in domains_infos:
                activated = json.loads(domains_infos[domain]['activated'].lower())
            if activated and domain not in extra_banned:
                spider.urls.append(url['objectID'])
        return spider

    def start_requests(self):

        for url in self.urls:
            yield scrapy.Request(url)

            if self.is_test_mode:
                break
