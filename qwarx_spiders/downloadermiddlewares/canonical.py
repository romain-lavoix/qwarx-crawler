# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import logging

from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.url import url_is_from_spider

logger = logging.getLogger(__name__)


class RelCanonicalMiddleware(object):
    _extractor = LinkExtractor(restrict_xpaths=['//head/link[@rel="canonical"]'], tags=['link'], attrs=['href'])

    def __init__(self):
        self.enabled = False

    @classmethod
    def from_crawler(cls, crawler):
        o = cls()
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        self.enabled = True

    def process_response(self, request, response, spider):
        if isinstance(response, HtmlResponse) and response.body and getattr(spider, 'follow_canonical_links', False):
            rel_canonical = self._extractor.extract_links(response)
            if rel_canonical:
                rel_canonical = rel_canonical[0].url
                if rel_canonical != request.url and url_is_from_spider(rel_canonical, spider):
                    logger.debug("Redirecting (rel=\"canonical\") to %s from %s", rel_canonical, request)
                    return request.replace(url=rel_canonical, callback=lambda r: r if r.status == 200 else response)
        return response
