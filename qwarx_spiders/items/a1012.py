# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader.processors import MapCompose

from .base import BaseIdItem, BaseMetaItem, BaseQwarxCrawlerItem
from ..utils.utils import TakeFirstAndEmpty, str_strip_allow_empty


class IdItem(BaseIdItem):
    pass


class MetaItem(BaseMetaItem):
    pass


class RichItem(scrapy.Item):
    """All custom fields will be added here"""

    address = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())
    category = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())
    tel1 = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())
    tel2 = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())


class A1012CrawlerItem(BaseQwarxCrawlerItem):
    pass
