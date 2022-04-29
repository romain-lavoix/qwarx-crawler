# -*- coding: utf-8 -*-

import json
import logging

import scrapy
from scrapy import signals

from ..base import BaseSpider
from ...services.algolia import AlgoliaSearchBase
from ...services.aws import AWSBase

logger = logging.getLogger(__name__)


class HealthCheck(scrapy.Spider, BaseSpider, AWSBase, AlgoliaSearchBase):
    """Check all urls from DB if return 404 and remove from DB """
    rotate_user_agent = True
    name = "health_check"
    allowed_domains = []
    start_urls = []
    bucket_size = 100

    custom_settings = {
        'ROBOTSTXT_OBEY': 'False',
        'RETRY_ENABLED': 'False'
    }

    # Put here all the status code that needs to be removed from Algolia DB
    STATUS_CODES_AS_BAD = ('404',)

    def __init__(self, *args, **kwargs):
        super(HealthCheck, self).__init__(HealthCheck, *args, **kwargs)
        self.aws_lambda = None
        self.urls_to_delete = []
        self.nb_urls_to_delete = 0
        self.nb_urls = 0
        self.nb_urls_processed = 0

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(HealthCheck, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        return spider

    def spider_opened(self, spider):
        self.aws_lambda = self.get_aws_lambda()

    def start_requests(self):
        urls = []
        for url in self.get_algolia_index().browse_all({"query": ""}):
            if len(urls) % 10000 == 0:
             logger.info('{} urls scanned from algolia'.format(len(urls)))
            if not url['objectID'].startswith('https://shop.nc/'):
                urls.append(url['objectID'])

        self.nb_urls = len(urls)
        for url in urls:
            self.nb_urls_processed = self.nb_urls_processed + 1
            yield scrapy.Request(url, callback=self.parse, method='HEAD',
                                 dont_filter=True,
                                 meta={'handle_httpstatus_all': True})
            if self.is_test_mode:
                break

    def parse(self, response):
        status_code = str(response.status)
        for exclude_status_code in self.STATUS_CODES_AS_BAD:
            exclude_status_code = str(exclude_status_code)

            if (exclude_status_code.endswith('xx') and status_code[0] == exclude_status_code[0]) or \
                (status_code == exclude_status_code):
                self.nb_urls_to_delete = self.nb_urls_to_delete + 1
                logger.info('adding {} to the list of urls to delete'.format(response.url))
                logger.info('404 count {} / {} urls processed / {} urls total'.format(self.nb_urls_to_delete,
                                                                                      self.nb_urls_processed,
                                                                                      self.nb_urls))
                self.urls_to_delete.append(response.url)

        if len(self.urls_to_delete) == self.bucket_size or (
                self.nb_urls != 0 and (self.nb_urls == self.nb_urls_processed)):
            logger.info('deleting from Algolia : {}'.format(', '.join(map(str, self.urls_to_delete))))
            algolia_index = self.get_algolia_index()
            algolia_index.delete_objects(self.urls_to_delete)
            self.urls_to_delete.clear()
