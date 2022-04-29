# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from ..utils.parse import get_domain


class DeltaFetchKeyUrlMiddleware(object):
    """Rotate user-agent for each request."""

    def __init__(self):
        self.enabled = False
        self.type = ''

    @classmethod
    def from_crawler(cls, crawler):
        o = cls()
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        deltafetch_key_url = getattr(spider, 'deltafetch_key_url', self.enabled)
        deltafetch_key_domain = getattr(spider, 'deltafetch_key_domain', self.enabled)
        self.enabled = deltafetch_key_url or deltafetch_key_domain
        self.type = 'url' if deltafetch_key_url else 'domain'

    def process_request(self, request, spider):
        if self.enabled:
            request.meta['deltafetch_key'] = request.url if self.type == 'url' else get_domain(request.url)
