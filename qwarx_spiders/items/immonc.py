# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

from .base import BaseIdItem, BaseMetaItem, BaseQwarxCrawlerItem, BaseRichItem
from ..utils.utils import TakeFirstAndEmpty, str_strip, clean_price


class IdItem(BaseIdItem):
    pass


class MetaItem(BaseMetaItem):
    pass


class RichItem(BaseRichItem):
    real_estate_type = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(clean_price), output_processor=TakeFirstAndEmpty())


class ImmoncCrawlerItem(BaseQwarxCrawlerItem):
    pass
