# -*- coding: utf-8 -*-
import itertools

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.utils.url import parse_url

from ..base import BaseSpider
from ...items.autos import AutosCrawlerItem
from ...items.autos import IdItem, MetaItem, RichItem
from ...utils.utils import str_strip


class AutosSpider(scrapy.Spider, BaseSpider):
    name = "autos"
    allowed_domains = ["autos.nc"]
    start_urls = ['http://autos.nc']

    custom_settings = {

    }
    general_info_map = {
        'année': 'year',
        'modèle': 'model2',
        'kilométrage': 'km',
        'puissance fiscale': 'power',
        'puissance': 'power2',
        'boite de vitesse': 'gear',
        'energie': 'energy',
        'commune': 'area',
    }

    search_url = '{}/rechercher?categories=&fuels=&localisations=&submit='.format(start_urls[0])

    def parse(self, response):
        """Submit search form to get all the results. For some reason we need to get all the results
        via search for because we get 400 response from cloudflare if we try to navigate the paginator on the
        home page"""

        yield response.follow(self.search_url, callback=self.parse_search_submit)

    def parse_search_submit(self, response):
        """Here we get results of a submit search form"""

        yield from self.parse_search_results(response)
        yield from self.parse_paginator(response)

    def parse_paginator(self, response):
        """Parse all the pages from the paginator"""

        for url in response.xpath('//ul[@class="pagination"]/li/a/@href').extract():

            yield response.follow(url, callback=self.parse_search_results)

            if self.is_test_mode:
                break

    def parse_search_results(self, response):
        """Parse all the results from the search"""

        for url in response.xpath('//div[contains(@class, "col-sm-6")]/a/@href').extract():
            yield response.follow(url, callback=self.parse_item)

            if self.is_test_mode:
                break

    def parse_item(self, response):
        """Extract single item from the page"""

        item_loader = ItemLoader(item=AutosCrawlerItem(), response=response)
        meta_item_loader = ItemLoader(item=MetaItem(), response=response)
        id_item_loader = ItemLoader(item=IdItem(), response=response)
        rich_item_loader = ItemLoader(item=RichItem(), response=response)

        page_url = response.url

        item_loader.add_value('objectID', page_url)

        meta_item_loader.add_xpath('description', '//meta[@property="og:description"]/@content')
        meta_item_loader.add_xpath('image', '//meta[@property="og:image"]/@content')

        id_item_loader.add_xpath('title', '//meta[@property="og:title"]/@content')
        id_item_loader.add_value('domain', parse_url(page_url).hostname)
        id_item_loader.add_value('url', page_url)

        rich_item_loader.add_xpath('price', '//span[@class="detail-price"]/text()')

        details_list = item_loader.get_xpath(
            '//div[contains(@class, "detail-infos-generales")]/descendant-or-self::div[span]/descendant-or-self::text()',
            MapCompose(str_strip, lambda x: x.strip(': ')))

        # Split list by 2 elements with details fields
        for detail_field, detail_value in itertools.zip_longest(*[iter(details_list)] * 2):
            rich_item_loader.add_value(self.general_info_map[detail_field.lower()], detail_value)

        item_loader.add_value('id', id_item_loader.load_item())
        item_loader.add_value('meta', meta_item_loader.load_item())
        item_loader.add_value('rich', rich_item_loader.load_item())

        yield item_loader.load_item()
