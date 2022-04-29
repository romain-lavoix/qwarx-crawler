# -*- coding: utf-8 -*-
from itertools import zip_longest

import scrapy
from furl import furl
from scrapy.http.response.html import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.utils.url import parse_url

from ..base import BaseSpider
from ...items.annuaire_plan import AnnuairePlanCrawlerItem
from ...items.annuaire_plan import IdItem, MetaItem, RichItem
from ...utils.utils import str_strip


class Annuaire_PlanSpider(scrapy.Spider, BaseSpider):
    name = "annuaire_plan"
    allowed_domains = ["annuaire.plan.nc"]
    start_urls = ['https://annuaire.plan.nc']
    custom_settings = {

    }

    def parse(self, response: HtmlResponse):

        yield from self.parse_categories(response)
        yield from self.parse_search_results(response)
        yield from self.parse_paginator(response)

    def parse_categories(self, response: HtmlResponse):
        """Parse all categories and subcategories"""

        # This xpath includes all the subcategories, so we don't need to go to categories
        # and then to subcategories
        xpath = '//ul[@id="taxo_menu"]/descendant-or-self::ul[@class="level-1"]/li/a'
        for link in LinkExtractor(restrict_xpaths=(xpath,)).extract_links(response):
            yield response.follow(link, callback=self.parse_paginator)

            if self.is_test_mode:
                break

    def parse_paginator(self, response: HtmlResponse):
        """Parse all the pages from the paginator"""

        yield from self.parse_search_results(response)

        last_page_url = response.xpath('//ul[@class="pager"]/li[last()]/a/@href').extract_first()
        if last_page_url:
            f = furl(last_page_url)
            max_pages = int(f.args['page'])

            self.logger.info("Found '%s' pages.", max_pages)

            for page in range(1, max_pages + 1):
                f.args['page'] = page
                yield response.follow(f.url, callback=self.parse_search_results)

                if self.is_test_mode:
                    break
        else:
            self.logger.info("No paginator for page: '%s'", response.url)

    def parse_search_results(self, response: HtmlResponse):
        """Parse all the results from the search"""

        xpath = '//article[@class="entreprise"]/descendant-or-self::div[@class="details"]/h2'

        for link in LinkExtractor(restrict_xpaths=(xpath,)).extract_links(response):
            yield response.follow(link, callback=self.parse_item)

            if self.is_test_mode:
                break

    def parse_item(self, response: HtmlResponse):
        """Extract single item from the page"""

        item_loader = ItemLoader(item=AnnuairePlanCrawlerItem(), response=response)
        meta_item_loader = ItemLoader(item=MetaItem(), response=response)
        id_item_loader = ItemLoader(item=IdItem(), response=response)
        rich_item_loader = ItemLoader(item=RichItem(), response=response)

        page_url = response.url

        item_loader.add_value('objectID', page_url)

        description = meta_item_loader.get_xpath(
            '//div[contains(@class, "views-field-field-activites")]/div/descendant-or-self::text()',
            MapCompose(str_strip))

        description_extra = meta_item_loader.get_xpath(
            '//div[h2[@class="fiche-ico_coordonnees"]]/div/descendant-or-self::text()',
            MapCompose(str_strip))

        description += [' '.join(i) for i in zip_longest(*[iter(description_extra)] * 2, fillvalue='')]

        meta_item_loader.add_xpath('image', '//img[contains(@class, "field-slideshow-image-1")]/@src')
        meta_item_loader.add_value('description', item_loader.get_value(description))

        id_item_loader.add_xpath('title', '//div[@class="view-content"]/div/h1/text()')
        id_item_loader.add_value('domain', parse_url(page_url).hostname)
        id_item_loader.add_value('url', page_url)

        rich_item_loader.add_xpath('category1', '//div[@class="breadcrumbfloat"][2]/a/span/text()')
        rich_item_loader.add_xpath('category2', '//div[@class="breadcrumbfloat"][3]/a/span/text()')
        rich_item_loader.add_xpath('hour',
                                   '//div[contains(@class, "active-opening-hours")]/div/descendant-or-self::text()')
        rich_item_loader.add_xpath('email', '//div[contains(@class, "field-adresse-email")]/div/a/text()')
        rich_item_loader.add_xpath('phone1', '//div[contains(@class, "field-telephone-standard")]/span/text()')
        rich_item_loader.add_xpath('phone2', '//div[contains(@class, "field-telephone-portable")]/span/text()')
        rich_item_loader.add_xpath('fax', '//div[contains(@class, "field-numero-de-fax")]/span/text()')
        rich_item_loader.add_xpath('text1', '//h2[@class="slogan"]/text()')

        item_loader.add_value('id', id_item_loader.load_item())
        item_loader.add_value('meta', meta_item_loader.load_item())
        item_loader.add_value('rich', rich_item_loader.load_item())

        yield item_loader.load_item()
