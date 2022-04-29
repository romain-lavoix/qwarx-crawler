# -*- coding: utf-8 -*-

import datetime
import time

from pytz import timezone
from scrapy.exceptions import DropItem


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids = set()
        self.crawl_timestamp = time.mktime(datetime.datetime.now(timezone('Pacific/Noumea')).date().timetuple())
        self.crawl_date = str(datetime.datetime.now(timezone('Pacific/Noumea')).date())

    def process_item(self, item, spider):
        if 'title' not in item['id']:
            raise DropItem("No title")
        title = item['id']['title']
        if title is None or len(title) == 0:
            raise DropItem("No title")

        item['crawl_date'] = self.crawl_date

        # duplication verification
        if not getattr(spider, 'check_duplicates', True):
            return item
        domain = item['id']['domain']
        title = item['id']['title']
        description = item['meta']['description'] if 'description' in item['meta'] else ''

        item_id = "{0}&&{1}&&{2}".format(domain, title, description)
        if item_id in self.ids:
            raise DropItem("Duplicate page")
        else:
            self.ids.add(item_id)
            return item
