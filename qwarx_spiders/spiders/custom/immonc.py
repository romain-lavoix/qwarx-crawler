# -*- coding: utf-8 -*-
from urllib.parse import urlencode

import scrapy
from furl import furl
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

from qwarx_spiders.spiders.base import BaseSpider
from ...items.immonc import ImmoncCrawlerItem
from ...items.immonc import IdItem, MetaItem, RichItem
from ...utils.parse import get_domain
from ...utils.utils import str_strip


class ImmoncSpider(scrapy.Spider, BaseSpider):
    name = 'immonc'
    allowed_domains = ['immonc.com']
    start_urls = ['https://www.immonc.com/']

    common_search_params = {
        'quartiers': '',
        'biens': '',
        'budget-min': '',
        'budget-max': '',
        'agence': '',
        'type': '1',
        'page': '1'
    }

    extra_details_fields_map = {
        'général': 'general',
        'quartier': 'quartier',
        'vue': 'view',
        'chambres': 'room',
        'cuisine': 'kitchen',
        'salle de bain': 'bathroom',
        'annexe': 'annexe',
        'garage': 'parking',
    }

    def parse(self, response):
        """Submit search for with option that we need to ensure that we search all the data"""

        search_url = response.xpath('//form[@id="quicksearch"]/@action').extract_first()

        for item_type_el in response.xpath('//select[@id="type_annonce"]/option'):
            item_type_name = item_type_el.xpath('text()').extract_first('').lower()
            item_type_value = item_type_el.xpath('@value').extract_first('')
            self.common_search_params['type'] = item_type_value
            search_params = urlencode(self.common_search_params)
            url = '{}/{}'.format(search_url, f'{item_type_name}?{search_params}')

            yield scrapy.FormRequest.from_response(response, url=url, formname='quicksearch',
                                                   callback=self.parse_paginator)

            if self.is_test_mode:
                break

    def parse_paginator(self, response):
        """Go to all the pages from the paginator and make sure we crawl all the results"""

        yield from self.parse_search_results(response)

        max_pages = response.xpath('//div[@class="listingpagination"]/strong/text()').re_first('Page \d+ sur (\d+)')

        if max_pages:
            url = response.url

            for page in range(2, int(max_pages) + 1):
                f = furl(url)
                f.args['page'] = page
                yield scrapy.Request(f.url, callback=self.parse_search_results)

                if self.is_test_mode:
                    break

        else:
            self.logger.debug(f"No paginator found for page: {response.url}")

    def parse_search_results(self, response):
        """Here we have a list of items and we need to access all of them and extract page information"""

        # for item_url in response.xpath('//div[@class="rel-listdet"]/descendant-or-self::h3/a/@href').extract():
        for item_el in response.xpath('//div[@class="rel-listdet"]/div/div/h3/a'):
            item_url = item_el.xpath('@href').extract_first()
            info_details = item_el.xpath('text()').extract_first('')
            room_nb = item_el.xpath('text()').re_first('.+?(F\d+.*)', '')

            meta = {
                'item': {
                    'item_type': info_details.split(' ', 1)[0],
                    'room_nb': room_nb
                },
                'deltafetch_key': item_url
            }
            yield response.follow(item_url, callback=self.parse_item, meta=meta)

            if self.is_test_mode:
                break

    def parse_item(self, response):
        """Extract all the fields for 1 item"""

        item = response.meta['item']

        item_loader = ItemLoader(item=ImmoncCrawlerItem(), response=response)
        meta_item_loader = ItemLoader(item=MetaItem(), response=response)
        id_item_loader = ItemLoader(item=IdItem(), response=response)
        rich_item_loader = ItemLoader(item=RichItem(), response=response)

        title_info = response.xpath('//div[@class="main-pagetitle"]/descendant-or-self::h2/text()').extract()

        if len(title_info) > 1:
            info_details, address_info = title_info
        else:
            # Address info is missing in this case
            info_details, address_info = title_info[0], ''

        info_details = info_details.strip()
        address_info = address_info.strip()

        # Here room_nb, item_type can be missing, handling this scenario
        info = ''
        if ' ' in info_details:
            info, _ = info_details.split(' ', 1)

        # Here as well we can have only city and no area
        city, area = '', ''
        if ' ' in address_info:
            city, address_info = address_info.split(' ', 1)
            if ' ' in address_info:
                _, area = address_info.rsplit(' ', 1)
        else:
            city = address_info

        page_url = response.url

        extra_details = {}

        for extra_details_el in response.xpath('//div[contains(@class, "prodettable")]/div/div[@class="gc_row"]/div'):
            details_title = extra_details_el.xpath('h4/text()').extract_first()
            _, detail_name = details_title.split(' ', 1)
            detail_name = detail_name.lower()

            details_text = '\n'.join(
                list(map(str_strip, extra_details_el.xpath('descendant-or-self::text()').extract())))

            if detail_name in self.extra_details_fields_map:
                extra_details[self.extra_details_fields_map[detail_name]] = details_text
            else:
                None
                # self.logger.warning("Extra details name: '%s' not defined in mappings: '%r' for page: '%s'",
                #                     detail_name,
                #                     self.extra_details_fields_map, page_url)

        item_loader.add_value('objectID', response.url)

        meta_item_loader.add_xpath('description', '//div[@class="prodet"]/descendant-or-self::text()')
        meta_item_loader.add_xpath('image', '//meta[@property="og:image"]/@content')

        id_item_loader.add_xpath('title', '//meta[@property="og:title"]/@content')
        id_item_loader.add_value('domain', get_domain(page_url))
        id_item_loader.add_value('url', page_url)

        rich_item_loader.add_value('price',
                                   item_loader.get_xpath('//div[@class="main-pagetitle"]/descendant-or-self::h4/text()',
                                                         TakeFirst()))
        # rich_item_loader.add_value('room_nb', item['room_nb'])
        rich_item_loader.add_value('real_estate_type', info)
        # rich_item_loader.add_value('city', city)
        # rich_item_loader.add_value('area', area)
        # rich_item_loader.add_value('details', extra_details)

        item_loader.add_value('id', id_item_loader.load_item())
        item_loader.add_value('meta', meta_item_loader.load_item())
        item_loader.add_value('rich', rich_item_loader.load_item())

        yield item_loader.load_item()
