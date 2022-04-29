# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader.processors import MapCompose

from .base import BaseIdItem, BaseMetaItem, BaseQwarxCrawlerItem
from ..utils.utils import str_strip, TakeFirstAndEmpty


class IdItem(BaseIdItem):
    pass


class MetaItem(BaseMetaItem):
    pass


class RichItem(scrapy.Item):
    """All custom fields will be added here"""

    price = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    year = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    brand = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    model = scrapy.Field(input_processor=MapCompose(lambda x: x.rsplit('–', 1)[0], str_strip),
                         output_processor=TakeFirstAndEmpty())
    type = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    energy = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    gear = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    color = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    km = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    mineral = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())


class OccasionsAutomobilesCrawlerItem(BaseQwarxCrawlerItem):
    pass
