# -*- coding: utf-8 -*-
import scrapy
from furl import furl
from scrapy.http.response.html import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.utils.url import parse_url

from ..base import BaseSpider
from ...items.petites_annonces import MetaItem, IdItem, RichItem
from ...items.petites_annonces import PetitesAnnoncesCrawlerItem


class Petites_AnnoncesSpider(scrapy.Spider, BaseSpider):
    name = "petites_annonces"
    allowed_domains = ["petites-annonces.nc"]
    start_urls = ['https://www.petites-annonces.nc']

    def parse(self, response: HtmlResponse):
        all_categories_url = response.xpath(
            '//div[@class="category-buttons"]/a[text()="toutes les categories"]/@href').extract_first()

        yield response.follow(all_categories_url, callback=self.parse_categories)

    def parse_categories(self, response: HtmlResponse):
        # xpath = '//div[@class="categorybox"][div[h4[contains(text(), "Véhicules")]]]'
        # Get all the categories
        xpath = '//div[@class="categorybox"]'

        for link in LinkExtractor(restrict_xpaths=(xpath,)).extract_links(response):
            yield response.follow(link, callback=self.parse_paginator)

            if self.is_test_mode:
                break

    def parse_paginator(self, response: HtmlResponse):
        """Parse all the pages from the paginator"""

        yield from self.parse_search_results(response)

        max_pages = response.xpath('//ul[@id="pager"]/li[last()]/a/text()').extract_first()
        if max_pages:
            for page in range(2, int(max_pages) + 1):
                f = furl(response.url)
                f.args['page'] = page
                yield response.follow(f.url, callback=self.parse_search_results)

                if self.is_test_mode:
                    break

    def parse_search_results(self, response: HtmlResponse):
        """Parse all the results from the search"""

        xpath = '//div[contains(@class, "productlistmain")]/div/a'

        for link in LinkExtractor(restrict_xpaths=(xpath,)).extract_links(response):
            yield response.follow(link, callback=self.parse_item)

            if self.is_test_mode:
                break

    def parse_item(self, response: HtmlResponse):
        """Extract single item from the page"""

        item_loader = ItemLoader(item=PetitesAnnoncesCrawlerItem(), response=response)
        meta_item_loader = ItemLoader(item=MetaItem(), response=response)
        id_item_loader = ItemLoader(item=IdItem(), response=response)
        rich_item_loader = ItemLoader(item=RichItem(), response=response)

        page_url = response.url

        item_loader.add_value('objectID', page_url)

        meta_item_loader.add_xpath('image', '//img[@id="main"]/@src')
        meta_item_loader.add_xpath('description', '//div[@class="addinfoetailpage"]/descendant-or-self::text()')
        meta_item_loader.add_xpath('date', '//div[@class="adlocationdate"]/span[1]/text()')

        id_item_loader.add_xpath('title', '//div[@class="ad-detail-info"]/h1/text()')
        id_item_loader.add_value('domain', parse_url(page_url).hostname)
        id_item_loader.add_value('url', page_url)

        rich_item_loader.add_xpath('category', '//div[@class="breadcrumb"]/ul/li/descendant-or-self::text()')
        rich_item_loader.add_xpath('price', '//div[@class="adprice"]/text()')
        rich_item_loader.add_xpath('phone', '//div[@class="addcontactinfodetailpage"]/span/text()')
        rich_item_loader.add_value('type', 'realestate' if 'Immobilier' in rich_item_loader.get_output_value(
            'category') else 'classified')

        item_loader.add_value('id', id_item_loader.load_item())
        item_loader.add_value('meta', meta_item_loader.load_item())
        item_loader.add_value('rich', rich_item_loader.load_item())

        yield item_loader.load_item()
