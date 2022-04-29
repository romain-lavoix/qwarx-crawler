# -*- coding: utf-8 -*-
import json
from datetime import datetime
from urllib.parse import urlencode

import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.loader import ItemLoader
from scrapy.utils.url import parse_url
from slugify import slugify

from ..base import BaseSpider
from ...items.argus import ArgusCrawlerItem
from ...items.argus import IdItem, MetaItem, RichItem


class ArgusSpider(scrapy.Spider, BaseSpider):
    name = "argus"
    allowed_domains = ["www.argus.nc"]
    start_urls = ['https://www.argus.nc']

    custom_settings = {
        'URLLENGTH_LIMIT': 600,
        'DOWNLOAD_TIMEOUT': 60
    }

    search_url = '{}/api/bid/light'.format(start_urls[0])

    page_size = 1000

    categories_map = {
        'CAR': 'autos',
        'MOTO': 'motos',
        'BOAT': 'bateaux'
    }

    common_search_params = {
        'customFilter': json.dumps({
            "modalBidOpened": False,
            "vehicleTypeCodes": list(categories_map.keys())
        }),
        'filter': json.dumps({
        }),
        'page': "0",
        'size': str(page_size),
        # 'sort': "risingDate,desc"
    }

    def make_ajax_request(self, url, callback, **kwargs):
        headers = {
            'X-Requested-With': 'XMLHttpRequest'
        }
        return scrapy.Request(url, headers=headers, callback=callback, **kwargs)

    def make_search_request(self, callback, page=0):
        """Submit search API and get json results."""

        self.common_search_params['page'] = str(page)

        url = '{}?{}'.format(self.search_url, urlencode(self.common_search_params))

        yield self.make_ajax_request(url, callback=callback)

    def _parse_json_response(self, response):
        """Validate if response is json and make sure we parse it."""

        try:
            return json.loads(response.body)
        except json.JSONDecodeError:
            self.logger.error("Error parsing response, not json.")
            raise CloseSpider("Invalid json response.")

    def parse(self, response):
        yield from self.make_search_request(self.parse_paginator, page=0)

    def parse_paginator(self, response):
        """Iterate over all the pages and make sure we get all the results"""

        json_data = self._parse_json_response(response)

        yield from self.parse_search_results(response)

        self.logger.info("Paginator: need to parse '%s' more pages.", json_data['totalPages'])

        for page in range(1, int(json_data['totalPages'])):
            yield from self.make_search_request(self.parse_search_results, page=page)

            if self.is_test_mode:
                break

    def parse_search_results(self, response):
        json_data = self._parse_json_response(response)

        self.logger.info("Found '%s' elements", json_data['numberOfElements'])

        for item in json_data['content']:
            yield from self.parse_item(item)

            if self.is_test_mode:
                break

    def parse_item(self, json_item, response=None):
        """Parse single item"""

        item_loader = ItemLoader(item=ArgusCrawlerItem(), response=response)
        meta_item_loader = ItemLoader(item=MetaItem(), response=response)
        id_item_loader = ItemLoader(item=IdItem(), response=response)
        rich_item_loader = ItemLoader(item=RichItem(), response=response)

        vehicle = json_item['vehicle']

        page_url = '{domain}/{category}/annonces/{slug}-{item_id}'.format(
            domain=self.start_urls[0],
            category=self.categories_map[vehicle['type']].lower(),
            slug=slugify(
                ' '.join((vehicle.get('brand', {}).get('label', ''), vehicle.get('model', {}).get('label', '')))),
            item_id=json_item['id']
        )

        image_url = "{}/{}".format(self.start_urls[0], json_item['photos'][0]['relativeLargeUrl']) if json_item[
            'photos'] else ''

        release_date = vehicle.get('releaseDate')

        item_loader.add_value('objectID', page_url)

        meta_item_loader.add_value('description', json_item.get('description', ''))
        meta_item_loader.add_value('image', image_url)

        title = "{brand} {model} - {year}".format(
            brand=vehicle.get('brand', {}).get('label', ''),
            model=vehicle.get('model', {}).get('label', ''),
            year=datetime.fromtimestamp(release_date / 1000.0).year if release_date else '',
        )

        id_item_loader.add_value('title', title)
        id_item_loader.add_value('domain', parse_url(page_url).hostname)
        id_item_loader.add_value('url', page_url)

        registration_number = vehicle.get('registrationNumber', '')

        rich_item_loader.add_value('model', vehicle.get('label', ''))
        rich_item_loader.add_value('mineral', 'Série {}'.format(registration_number) if registration_number else '')
        rich_item_loader.add_value('price', json_item.get('formatPrice', ''))
        rich_item_loader.add_value('area', json_item.get('user', {}).get('reseller', {}).get('name', ''))
        rich_item_loader.add_value('gear', vehicle.get('transmission', {}).get('label', ''))
        rich_item_loader.add_value('computer', '{} km'.format(vehicle.get('nbKm', '')))
        rich_item_loader.add_value('energy', vehicle.get('engine', {}).get('energy', {}).get('label'))

        item_loader.add_value('id', id_item_loader.load_item())
        item_loader.add_value('meta', meta_item_loader.load_item())
        item_loader.add_value('rich', rich_item_loader.load_item())

        yield item_loader.load_item()
