# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

from ..utils.utils import str_strip, str_strip_allow_empty, TakeFirstAndEmpty, clean_html, limit_description, \
    limit_title, clear, remove_newlines, output_description, parse_date, parse_date_human, base64_check, clean_url, \
    clean_price


class BaseMetaItem(scrapy.Item):
    image = scrapy.Field(input_processor=MapCompose(str_strip, base64_check), output_processor=TakeFirst())
    date = scrapy.Field(input_processor=MapCompose(str_strip, parse_date), output_processor=TakeFirst())
    description = scrapy.Field(
        input_processor=MapCompose(str_strip, clean_html, clear, remove_newlines, limit_description),
        output_processor=output_description)
    redirect_urls = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirst())


class BaseIdItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(str_strip_allow_empty, clean_html, clear, remove_newlines, limit_title),
        output_processor=TakeFirstAndEmpty())
    domain = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirst())
    url = scrapy.Field(input_processor=MapCompose(str_strip, clean_url), output_processor=TakeFirst())


class BaseRichItem(scrapy.Item):
    date = scrapy.Field(input_processor=MapCompose(str_strip, parse_date_human), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(clear, clean_price), output_processor=TakeFirst())
    real_estate_type = scrapy.Field(input_processor=MapCompose(str_strip), output_processor=TakeFirst())
    location = scrapy.Field(output_processor=TakeFirst())


class BaseBoostItem(scrapy.Item):
    homepage = scrapy.Field(output_processor=TakeFirst())
    external_links = scrapy.Field(output_processor=TakeFirst())
    links_to_domain = scrapy.Field(output_processor=TakeFirst())
    domain_authority = scrapy.Field(output_processor=TakeFirst())
    url_length = scrapy.Field(output_processor=TakeFirst())
    image = scrapy.Field(output_processor=TakeFirst())
    meta_description = scrapy.Field(output_processor=TakeFirst())


class BaseQwarxCrawlerItem(scrapy.Item):
    objectID = scrapy.Field(input_processor=MapCompose(clean_url), output_processor=TakeFirst())
    crawl_date = scrapy.Field(input_processor=MapCompose(), output_processor=TakeFirst())
    id = scrapy.Field(output_processor=TakeFirst())
    meta = scrapy.Field(output_processor=TakeFirst())
    rich = scrapy.Field(output_processor=TakeFirst())
    boost = scrapy.Field(output_processor=TakeFirst())
    category = scrapy.Field(output_processor=TakeFirst())
    spider_name = scrapy.Field(output_processor=TakeFirst())
