# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.utils.url import parse_url

from ..base import BaseSpider
from ...items.occasions_automobiles import MetaItem, IdItem, RichItem
from ...items.occasions_automobiles import OccasionsAutomobilesCrawlerItem
from ...utils.utils import str_strip


class OccasionsAutomobilesSpider(scrapy.Spider, BaseSpider):
    name = "occasions_automobiles"
    allowed_domains = ["occasions-automobiles.nc"]
    start_urls = ['https://occasions-automobiles.nc']

    custom_settings = {
    }

    search_url = 'http://occasions-automobiles.nc/parc-auto/page/{page_num}/?sort_order=price_low'

    details_map = {
        'type': 'type',
        'carburant': 'energy',
        'transmission': 'gear',
        'couleur extérieure': 'color',
        'kilométrage': 'km',
        'immatriculation': 'mineral',
    }

    def parse(self, response):
        """Make search request for all items"""
        url = self.search_url.format(page_num=1)

        yield response.follow(url, callback=self.parse_paginator)

    def parse_paginator(self, response):
        """Get all the pages from paginator"""
        yield from self.parse_search_results(response)

        try:
            max_pages = int(response.xpath('//a[@class="page-numbers"]/text()').extract()[-1])
            for page in range(2, int(max_pages)):
                url = self.search_url.format(page_num=page)
                yield response.follow(url, callback=self.parse_search_results)

                if self.is_test_mode:
                    break

        except Exception as e:
            self.logger.error("Issues with paginator: %s" % e)

    def parse_search_results(self, response):
        """Parse all the results from the search"""

        link_extractor = LinkExtractor(allow=('/listings/',))
        for link in link_extractor.extract_links(response):
            yield response.follow(link, callback=self.parse_item)

            if self.is_test_mode:
                break

    def parse_item(self, response):
        """Extract single item from the page"""

        item_loader = ItemLoader(item=OccasionsAutomobilesCrawlerItem(), response=response,
                                 selector=response.xpath('//div[@class="single-listing-car-inner"]'))
        meta_item_loader = ItemLoader(item=MetaItem(), response=response)
        id_item_loader = ItemLoader(item=IdItem(), response=response)
        rich_item_loader = ItemLoader(item=RichItem(), response=response)

        page_url = response.url

        item_loader.add_value('objectID', page_url)

        meta_item_loader.add_xpath('image', '//meta[@property="og:image"]/@content')
        meta_item_loader.add_xpath('description', '//meta[@property="og:description"]/@content')

        id_item_loader.add_xpath('title', '//div[contains(@class, "listing-single-price-title")]'
                                          '/div[@class="title"]/div/text()')
        id_item_loader.add_value('domain', parse_url(page_url).hostname)
        id_item_loader.add_value('url', page_url)

        rich_item_loader.add_xpath('price',
                                   '//div[contains(@class, "listing-single-price-title")]/div[@class="price"]/text()')
        rich_item_loader.add_xpath('year',
                                   '//div[contains(@class, "listing-single-price-title")]/div[@class="title"]/text()')
        rich_item_loader.add_xpath('brand', '//span[@property="itemListElement"][3]/a/span/text()')
        rich_item_loader.add_xpath('model', '//span[@property="itemListElement"][4]/span/text()')

        # Extract all the other details and map to proper fields
        for details_row_el in response.xpath(
                '//table[@class="stm-table-main"]/descendant-or-self::table[@class="inner-table"]/tr'):
            details_field, details_value = item_loader.get_value(details_row_el.xpath('td/text()').extract(),
                                                                 MapCompose(str_strip))
            details_field = details_field.lower()

            if not self.crawler.stats.get_value(details_field):
                rich_item_loader.add_value(self.details_map[details_field], details_value)
                self.crawler.stats.set_value(details_field, details_value)
            else:
                self.logger.warning("Field '%s' not found in mapping for url '%s'", details_value, page_url)

        item_loader.add_value('id', id_item_loader.load_item())
        item_loader.add_value('meta', meta_item_loader.load_item())
        item_loader.add_value('rich', rich_item_loader.load_item())

        yield item_loader.load_item()
