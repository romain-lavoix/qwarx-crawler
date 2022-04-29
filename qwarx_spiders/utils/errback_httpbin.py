# -*- coding: utf-8 -*-

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError


def errback_httpbin(self, failure):
    # log all errback failures,
    # in case you want to do something special for some errors,
    # you may need the failure's type

    # if isinstance(failure.value, HttpError):
    if failure.check(HttpError):
        # you can get the response
        response = failure.value.response
        self.logger.error('HttpError on %s', response.url)

    # elif isinstance(failure.value, DNSLookupError):
    elif failure.check(DNSLookupError):
        # this is the original request
        request = failure.request
        # self.logger.error('DNSLookupError on %s', request.url)

    # elif isinstance(failure.value, TimeoutError):
    elif failure.check(TimeoutError):
        request = failure.request
        self.logger.error('TimeoutError on %s', request.url)

    else:
        self.logger.error(repr(failure))
