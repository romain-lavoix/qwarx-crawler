# -*- coding: utf-8 -*-

from itertools import zip_longest

import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.utils.url import parse_url

from ..base import BaseSpider
from ...items.legratuit import LegratuitCrawlerItem
from ...items.legratuit import MetaItem, IdItem, RichItem
from ...utils.utils import str_strip


class LegratuitSpider(scrapy.Spider, BaseSpider):
    name = "legratuit"
    allowed_domains = ["legratuit.nc"]
    start_urls = ['https://legratuit.nc']

    custom_settings = {

    }
    caracteristic_maps = {
        'nombre de places de parking': 'parking',
        'nombre de pièce(s)': 'room_nb',
        'nombre de chambre(s)': 'bedroom_nb',
        'surface': 'surface',
        'vue': 'view',
        'meuble': 'furniture',
        'collocation': 'colocation',
        'entreprise': 'entreprise',
    }

    def parse(self, response: HtmlResponse):
        yield from self.parse_search_results(response)
        yield from self.parse_paginator(response)

    def parse_paginator(self, response: HtmlResponse):
        """Parse all the pages from the paginator"""

        max_pages = response.xpath('//div[@id="pagination"]/div/a[last()]/@href').extract_first('').strip('/')

        self.logger.info("Found '%s' pages", max_pages)

        for page in range(2, int(max_pages) + 1):
            url = '{}/{}'.format(self.start_urls[0], page)
            yield response.follow(url, callback=self.parse_search_results)

            if self.is_test_mode:
                break

    def parse_search_results(self, response: HtmlResponse):
        """Parse all the results from the search"""

        for item_url in response.xpath('//div[@class="title-price"]/a/@href').extract():
            yield response.follow(item_url, callback=self.parse_item)

            if self.is_test_mode:
                break

    def parse_item(self, response: HtmlResponse):
        """Extract single item from the page"""

        item_loader = ItemLoader(item=LegratuitCrawlerItem(), response=response)
        meta_item_loader = ItemLoader(item=MetaItem(), response=response)
        id_item_loader = ItemLoader(item=IdItem(), response=response)
        rich_item_loader = ItemLoader(item=RichItem(), response=response)

        page_url = response.url

        item_loader.add_value('objectID', page_url)

        meta_item_loader.add_xpath('image', '//meta[@property="og:image"]/@content')
        meta_item_loader.add_xpath('description', '//meta[@property="og:description"]/@content')

        id_item_loader.add_xpath('title', '//section/header/div/h1/text()')
        id_item_loader.add_value('domain', parse_url(page_url).hostname)
        id_item_loader.add_value('url', page_url)

        rich_item_loader.add_xpath('price', '//p[contains(@class, "price")]/text()')
        rich_item_loader.add_xpath('category1', '//h3[@class="ui-title"]/span[3]/a/text()')
        rich_item_loader.add_xpath('category2', '//h3[@class="ui-title"]/span[5]/a/text()')
        rich_item_loader.add_xpath('accomodation1', '//div[h4[text()="Rangements"]]/div/descendant-or-self::text()')
        rich_item_loader.add_xpath('accomodation2', '//div[h4[text()="Commodités"]]/div/descendant-or-self::text()')
        rich_item_loader.add_xpath('date', '//p[@class="publish"]/text()')

        # get localisation data
        localisation = rich_item_loader.get_xpath('//div[contains(@class, "localisation")]/p/text()',
                                                  MapCompose(lambda x: x.split('-'), str_strip))

        for area1, area2, area3 in zip_longest(*[iter(localisation)] * 3, fillvalue=''):
            rich_item_loader.add_value('area1', area1)
            rich_item_loader.add_value('area2', area2)
            rich_item_loader.add_value('area3', area3)
            break

        # Get caracteristics data
        caracteristics = rich_item_loader.get_xpath('//div[@id="caracteristics"]/div/descendant-or-self::text()',
                                                    MapCompose(str_strip, lambda x: x.strip(':'), str_strip))

        for field_name, field_value in zip_longest(*[iter(caracteristics)] * 2, fillvalue=''):
            field_name = field_name.lower()
            if field_name in self.caracteristic_maps:
                rich_item_loader.add_value(self.caracteristic_maps[field_name], field_value)
            else:
                if not self.crawler.stats.get_value(field_name):
                    self.logger.warning("Field name not found in caracteristics mapping: '%s', on page: '%s'",
                                        field_name, page_url)
                    self.crawler.stats.set_value(field_name, field_value)

        item_loader.add_value('id', id_item_loader.load_item())
        item_loader.add_value('meta', meta_item_loader.load_item())
        item_loader.add_value('rich', rich_item_loader.load_item())

        yield item_loader.load_item()
