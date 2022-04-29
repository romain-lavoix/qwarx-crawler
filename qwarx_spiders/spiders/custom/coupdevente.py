# -*- coding: utf-8 -*-

import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

from ..base import BaseSpider
from ...items.coupdevente import CoupdeventeCrawlerItem
from ...items.coupdevente import IdItem, MetaItem, RichItem
from ...utils.parse import get_domain


class CoupdeventeSpider(scrapy.Spider, BaseSpider):
    name = "coupdevente"
    allowed_domains = ["coupdevente.nc"]
    start_urls = ['http://coupdevente.nc']

    paginator_url = 'http://coupdevente.nc/offres/Caledonie/page-{page}/'

    def parse(self, response):
        yield response.follow('http://coupdevente.nc/offres/Caledonie/', callback=self.parse_paginator)

    def parse_paginator(self, response: HtmlResponse):
        """Parse all the pages from the paginator"""

        yield from self.parse_search_results(response)

        max_pages = response.xpath('//div[@class="lstpages"]/a[last()]/@href').re_first('page-(\d+)')

        for page in range(2, int(max_pages) + 1):
            url = self.paginator_url.format(page=page)
            yield response.follow(url, callback=self.parse_search_results)

            if self.is_test_mode:
                break

    def parse_search_results(self, response: HtmlResponse):
        """Parse all the results from the search"""

        for link in LinkExtractor(restrict_xpaths=('//td[@class="tdtitl"]',)).extract_links(response):
            yield response.follow(link, callback=self.parse_item, meta={'deltafetch_key': link.url})

            if self.is_test_mode:
                break

    def parse_item(self, response: HtmlResponse):
        """Extract single item from the page"""

        item_loader = ItemLoader(item=CoupdeventeCrawlerItem(), response=response)
        meta_item_loader = ItemLoader(item=MetaItem(), response=response)
        id_item_loader = ItemLoader(item=IdItem(), response=response)
        rich_item_loader = ItemLoader(item=RichItem(), response=response)

        page_url = response.url

        item_loader.add_value('objectID', page_url)

        meta_item_loader.add_xpath('description', '//span[@itemprop="description"]/text()')
        meta_item_loader.add_xpath('image', '//a[@itemprop="contentURL"]/@href')
        meta_item_loader.add_xpath('date', '//div[@itemprop="offers"]/text()[last()-1]')

        id_item_loader.add_xpath('title', '//span[@itemprop="name"]/text()')
        id_item_loader.add_value('domain', get_domain(page_url))
        id_item_loader.add_value('url', page_url)

        rich_item_loader.add_xpath('price', '//span[@itemprop="price"]/text()')
        rich_item_loader.add_xpath('category1', '//div[@id="bannierec"]/a[2]/text()')
        rich_item_loader.add_xpath('category2', '//div[@id="bannierec"]/a[3]/text()')
        rich_item_loader.add_xpath('area', '//div[@id="bannierec"]/a[4]/text()')

        item_loader.add_value('id', id_item_loader.load_item())
        item_loader.add_value('meta', meta_item_loader.load_item())
        item_loader.add_value('rich', rich_item_loader.load_item())

        return item_loader.load_item()
