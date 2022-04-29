import scrapy
from scrapy.loader.processors import MapCompose
from scrapy.loader.processors import TakeFirst

from .base import BaseIdItem, BaseMetaItem, BaseQwarxCrawlerItem
from ..utils.parse_date.wamland import parse_date
from ..utils.utils import str_strip, TakeFirstAndEmpty, clear, remove_newlines


def filter_price(value):
    if value is None:
        value = ""
    else:
        value = value.replace(",", ".")

    return value


class IdItem(BaseIdItem):
    pass


class MetaItem(BaseMetaItem):
    date = scrapy.Field(input_processor=MapCompose(str_strip, parse_date), output_processor=TakeFirstAndEmpty())


class RichItem(scrapy.Item):
    product_category = scrapy.Field(input_processor=MapCompose(clear, remove_newlines), output_processor=TakeFirst())
    product_type = scrapy.Field(input_processor=MapCompose(clear, remove_newlines), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(clear, remove_newlines), output_processor=TakeFirst())
    images = scrapy.Field(input_processor=MapCompose(clear, remove_newlines), output_processor=TakeFirst())


class WamlandItem(BaseQwarxCrawlerItem):
    pass
