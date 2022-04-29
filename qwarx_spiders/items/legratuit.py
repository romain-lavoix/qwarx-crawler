# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader.processors import MapCompose, Join

from .base import BaseIdItem, BaseMetaItem, BaseQwarxCrawlerItem, BaseRichItem
from ..utils.legratuit import parse_date
from ..utils.utils import str_strip, TakeFirstAndEmpty


class IdItem(BaseIdItem):
    pass


class MetaItem(BaseMetaItem):
    pass


class RichItem(BaseRichItem):
    """All custom fields will be added here"""

    date = scrapy.Field(input_processor=MapCompose(str_strip, parse_date), output_processor=TakeFirstAndEmpty())
    price = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    category1 = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    category2 = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    accomodation1 = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=Join('\n'))
    accomodation2 = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=Join('\n'))
    area1 = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    area2 = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    area3 = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    parking = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    room_nb = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    bedroom_nb = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    surface = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    view = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    furniture = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    colocation = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    entreprise = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())
    date = scrapy.Field(input_processor=MapCompose(str_strip, parse_date), output_processor=TakeFirstAndEmpty())


class LegratuitCrawlerItem(BaseQwarxCrawlerItem):
    pass
