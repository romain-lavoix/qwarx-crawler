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

    price = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())
    year = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())
    model2 = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())
    km = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())
    power = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())
    power2 = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())
    gear = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())
    energy = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())
    area = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())


class AutosCrawlerItem(BaseQwarxCrawlerItem):
    pass
