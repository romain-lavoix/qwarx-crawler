# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader.processors import MapCompose

from .base import BaseIdItem, BaseMetaItem, BaseQwarxCrawlerItem
from ..utils.parse_date.coupdevente import parse_date
from ..utils.utils import str_strip, TakeFirstAndEmpty


class IdItem(BaseIdItem):
    pass


class MetaItem(BaseMetaItem):
    date = scrapy.Field(input_processor=MapCompose(str_strip, parse_date), output_processor=TakeFirstAndEmpty())


class RichItem(scrapy.Item):
    """All custom fields will be added here"""

    price = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    category1 = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    category2 = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    area = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())


class CoupdeventeCrawlerItem(BaseQwarxCrawlerItem):
    pass
