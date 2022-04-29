# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader.processors import MapCompose, Join

from .base import BaseIdItem, BaseMetaItem, BaseQwarxCrawlerItem
from ..utils.utils import TakeFirstAndEmpty, str_strip_allow_empty, str_strip


class IdItem(BaseIdItem):
    pass


class MetaItem(BaseMetaItem):
    pass


class RichItem(scrapy.Item):
    """All custom fields will be added here"""

    category1 = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())
    category2 = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())
    hour = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=Join('\n'))
    email = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())
    phone1 = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())
    phone2 = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())
    fax = scrapy.Field(input_processor=MapCompose(str_strip_allow_empty), output_processor=TakeFirstAndEmpty())
    text1 = scrapy.Field(input_processor=MapCompose(str_strip, lambda x: x.strip('"')),
                         output_processor=TakeFirstAndEmpty())


class AnnuairePlanCrawlerItem(BaseQwarxCrawlerItem):
    pass
