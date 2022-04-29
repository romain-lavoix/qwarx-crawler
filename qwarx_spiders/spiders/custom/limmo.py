# -*- coding: utf-8 -*-
import scrapy
from furl import furl
from scrapy.http.response.html import HtmlResponse
from scrapy.loader import ItemLoader
from scrapy.utils.url import parse_url

from ..base import BaseSpider
from ...items.limmo import LimmoCrawlerItem
from ...items.limmo import MetaItem, IdItem, RichItem


class LimmoSpider(scrapy.Spider, BaseSpider):
    name = "limmo"
    allowed_domains = ["limmo.nc"]
    start_urls = ['http://www.limmo.nc']

    items_per_page = 25

    def parse(self, response: HtmlResponse):
        for url in response.xpath('//ul/li/a[span[text()="Location" or text()="Vente"]]/@href').extract():
            yield response.follow(url, callback=self.parse_paginator)

    def parse_paginator(self, response: HtmlResponse):
        """Parse all the pages from the paginator"""

        yield from self.parse_search_results(response)

        last_page_url = response.xpath('//div[@class="pagination"]/input[last()]/@onclick').re_first('.+?\'(.+)\'')

        f = furl(last_page_url)
        max_pages = int(f.args['start'])

        self.logger.info("Found '%s' pages.", max_pages)

        for page_offset in range(self.items_per_page, max_pages + 1, self.items_per_page):
            f.args['start'] = page_offset
            yield response.follow(f.url, callback=self.parse_search_results)

            if self.is_test_mode:
                break

    def parse_search_results(self, response: HtmlResponse):
        """Parse all the results from the search"""

        for item_el in response.xpath('//table[@class="dj-items"]/descendant-or-self::tr[position() > 1]'):
            rich_item_loader = ItemLoader(item=RichItem(), selector=item_el, response=response)

            rich_item_loader.add_xpath('room_nb', 'td[@class="name"]/h3/a/text()')
            rich_item_loader.add_xpath('type', 'td[@class="cat_name"]/a/text()')
            rich_item_loader.add_xpath('city', 'td[@class="region"]/a/text()')
            rich_item_loader.add_xpath('price', 'td[@class="price"]/span[1]/text()')

            url = item_el.xpath('td[1]/a/@href').extract_first()
            yield response.follow(url, callback=self.parse_item,
                                  meta={'rich_item': rich_item_loader.load_item(),
                                        'deltafetch_key': url
                                        })

            if self.is_test_mode:
                break

    def parse_item(self, response: HtmlResponse):
        """Extract single item from the page"""

        item_loader = ItemLoader(item=LimmoCrawlerItem(), response=response)
        meta_item_loader = ItemLoader(item=MetaItem(), response=response)
        id_item_loader = ItemLoader(item=IdItem(), response=response)
        rich_item_loader = ItemLoader(item=RichItem(), response=response)

        page_url = response.url

        item_loader.add_value('objectID', page_url)

        meta_item_loader.add_xpath('image', '//meta[@property="og:image"]/@content')
        meta_item_loader.add_xpath('description', '//div[@class="description"]/descendant-or-self::text()')

        id_item_loader.add_xpath('title', '//meta[@property="og:title"]/@content')
        id_item_loader.add_value('domain', 'limmo.nc')
        id_item_loader.add_value('url', page_url)

        rich_item_loader.add_xpath('surface',
                                   '//div[contains(@class, "row_surface_en_m2")]/span[@class="row_value"]/text()')
        rich_item_loader.add_value('info', page_url.split('/', 4)[3])
        rich_item_loader.add_value(None, response.meta['rich_item'])

        item_loader.add_value('id', id_item_loader.load_item())
        item_loader.add_value('meta', meta_item_loader.load_item())
        item_loader.add_value('rich', rich_item_loader.load_item())

        yield item_loader.load_item()
