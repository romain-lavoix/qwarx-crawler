# -*- coding: utf-8 -*-
import json
import urllib.parse
from collections import OrderedDict

import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.loader import ItemLoader
from scrapy.utils.url import parse_url
from slugify import slugify

from ..base import BaseSpider
from ...items.a1012 import A1012CrawlerItem
from ...items.a1012 import MetaItem, IdItem, RichItem

# Place the content of file 'api_page_keys.json' here
API_KEYS = {}


class A1012Spider(scrapy.Spider, BaseSpider):
    name = "1012"
    allowed_domains = ["1012.nc"]
    start_urls = ['https://www.1012.nc']

    _api_keys = {}

    custom_settings = {
        'API_PAGE_SIZE': 1900,
        'DOWNLOAD_DELAY': 0.3
    }

    @property
    def api_page_size(self):
        return self.settings.getint('API_PAGE_SIZE')

    @property
    def api_keys(self):
        if not self._api_keys:
            if API_KEYS:
                self._api_keys = API_KEYS
            else:
                from qwarx_spiders.scripts.a1012.api_page_keys import API_PAGE_KEYS
                self._api_keys = API_PAGE_KEYS

        return self._api_keys

    def make_api_request(self, api_type, callback, params):
        # TODO@geo Check how X-RS is constructed
        headers = {
            'X-RS': params.pop('X-RS'),
        }

        url = 'https://www.1012.nc/api/v1/{api_type}?{params}'.format(
            api_type=api_type,
            params=urllib.parse.urlencode(params)
        )

        meta = {
            'api_type': api_type,
            'url_type': self.api_keys[api_type]['url_type']
        }
        return scrapy.Request(url, callback=callback, headers=headers, meta=meta)

    def to_json(self, response):
        try:
            return json.loads(response.body)
        except Exception as e:
            self.logger.error(e)

    def parse(self, response: HtmlResponse):
        for api_type, params_info in self.api_keys.items():
            for commune_name, commune_search_queries in params_info['items'].items():
                for search_query, page_infos in commune_search_queries.items():
                    for page_info in page_infos['pages']:
                        params = []

                        if api_type in ('pagesjaunes',):
                            params.append(('label', search_query))
                        else:
                            params.append(('name', search_query))

                        params += [
                            ('town', commune_name),
                            ('type', 'ALL'),
                            ('page', int(page_info['page']) - 1),  # zero indexed,
                            ('size', page_info['size']),
                            ('X-RS', page_info['key']),
                        ]

                        yield self.make_api_request(api_type, callback=self.parse_paginator, params=OrderedDict(params))

                        if self.is_test_mode:
                            break
                    if self.is_test_mode:
                        break
                if self.is_test_mode:
                    break
            if self.is_test_mode:
                break

    def parse_paginator(self, response: HtmlResponse):
        """Parse all the pages from the paginator"""

        yield from self.parse_search_results(response)

    def parse_search_results(self, response: HtmlResponse):
        """Parse all the results from the search"""

        json_data = self.to_json(response)

        for item in json_data:
            yield from self.parse_item(response, item)

            if self.is_test_mode:
                break

    def parse_item(self, response: HtmlResponse, item: dict):
        """Extract single item from the page"""

        item_id = item.get('regroupementId', None)
        mobile_url = ''
        if not item_id:
            item_id = item['numeros'][0]['id']
            mobile_url = 'mobilis/'

        url_type = response.meta['url_type']

        item_loader = ItemLoader(item=A1012CrawlerItem(), response=response)
        meta_item_loader = ItemLoader(item=MetaItem(), response=response)
        id_item_loader = ItemLoader(item=IdItem(), response=response)
        rich_item_loader = ItemLoader(item=RichItem(), response=response)

        page_url = 'https://www.1012.nc/{url_type}/{mobile_url}details/{item_id}/{slug}'.format(
            url_type=url_type,
            item_id=item_id,
            slug=slugify(item['libelle'], separator="_"),
            mobile_url=mobile_url
        )

        item_loader.add_value('objectID', page_url)

        id_item_loader.add_value('title', item['libelle'])
        id_item_loader.add_value('domain', parse_url(page_url).hostname)
        id_item_loader.add_value('url', page_url)

        if 'adresseGeophysique' in item:
            address = '{adresseGeophysique}, {cp}, {communeRaccordement}'.format(**item)
        else:
            address = ''
        rich_item_loader.add_value('address', address)
        rich_item_loader.add_value('category', ', '.join(item.get('rubriques', [])))

        for i, telephone_number in enumerate(item.get('numeros', []), 1):
            rich_item_loader.add_value('tel%s' % i, telephone_number.get('tel', ''))
            if i >= 2:
                break

        item_loader.add_value('id', id_item_loader.load_item())
        item_loader.add_value('meta', meta_item_loader.load_item())
        item_loader.add_value('rich', rich_item_loader.load_item())

        yield item_loader.load_item()
