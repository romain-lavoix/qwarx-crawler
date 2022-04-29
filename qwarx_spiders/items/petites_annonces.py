# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join

from .base import BaseIdItem, BaseMetaItem, BaseRichItem, BaseQwarxCrawlerItem
from ..utils.parse_date.petites_annonces import parse_date
from ..utils.utils import str_strip, str_strip_allow_empty, TakeFirstAndEmpty


class IdItem(BaseIdItem):
    pass


class MetaItem(BaseMetaItem):
    date = scrapy.Field(input_processor=MapCompose(str_strip, parse_date),
                        output_processor=TakeFirstAndEmpty())


class RichItem(BaseRichItem):
    price = scrapy.Field(
        input_processor=MapCompose(str_strip_allow_empty, lambda x: x.split(':', 1)[-1].split('/', 1)[0],
                                   str_strip_allow_empty), output_processor=TakeFirstAndEmpty())
    type = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirst())

    category = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=Join('/'))
    phone = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirstAndEmpty())


class PetitesAnnoncesCrawlerItem(BaseQwarxCrawlerItem):
    pass
