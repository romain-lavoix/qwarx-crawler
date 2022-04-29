# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader.processors import MapCompose

from .base import BaseIdItem, BaseMetaItem, BaseQwarxCrawlerItem
from ..utils.utils import TakeFirstAndEmpty, str_strip_allow_empty, clean_price


class IdItem(BaseIdItem):
    pass


class MetaItem(BaseMetaItem):
    pass


class RichItem(scrapy.Item):
    """All custom fields will be added here"""

    section1 = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())
    real_estate_type = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())
    bien = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())
    type = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())
    ville = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())
    quartier = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())
    price = scrapy.Field(input_processor=MapCompose(clean_price), output_processor=TakeFirstAndEmpty())
    date = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())


class ImmobilierCrawlerItem(BaseQwarxCrawlerItem):
    pass
