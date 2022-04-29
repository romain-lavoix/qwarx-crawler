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

    surface = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    info = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    room_nb = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    city = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    price = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    type = scrapy.Field(input_processor=MapCompose(str_strip, lambda x: x.split(' ', 1)),
                        output_processor=TakeFirstAndEmpty())


class LimmoCrawlerItem(BaseQwarxCrawlerItem):
    pass
