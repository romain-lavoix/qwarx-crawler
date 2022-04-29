# -*- coding: utf-8 -*-
import json
import textwrap
from urllib.parse import urlencode

import collections
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.loader import ItemLoader
from scrapy.utils.url import parse_url
from slugify import slugify

from ..base import BaseSpider
from ...items.bienmeloger import BienmelogerCrawlerItem
from ...items.bienmeloger import IdItem, MetaItem, RichItem


class BienmelogerSpider(scrapy.Spider, BaseSpider):
    name = "bienmeloger"
    allowed_domains = ["bienmeloger.nc"]
    start_urls = ['https://www.bienmeloger.nc']

    custom_settings = {
        'URLLENGTH_LIMIT': 600,
        'DOWNLOAD_TIMEOUT': 60
    }

    search_url = '{}/api/bid/light'.format(start_urls[0])

    page_size = 1000

    common_search_params = {
        'customFilter': json.dumps({
            "localizationIds": [],
            "statusIds": [],
            "realtyCategoryIds": [],
            "realtyTypeIds": [],
            "typeIds": [],
            "minPrice": "",
            "maxPrice": ""
        }),
        'filter': json.dumps({
            "isAvailable": True
        }),
        'page': "0",
        'size': str(page_size),
        # 'sort': "risingDate,desc"
    }

    # id: label from json response
    details_map = {
        1: 'Type de construction',
        3: 'Etage',
        4: 'Loft',
        5: 'Mezzanine',
        6: 'Plain-pied',
        7: 'En Duplex',
        8: 'En Triplex',
        9: 'Vue',
        10: 'Proche centre ville',
        11: 'Proche écoles',
        12: 'Proche commerces',
        13: 'Proche de la plage',
        14: 'En bord de mer',
        15: 'Quartier calme',
        16: 'Quartier résidentiel',
        18: 'Chambres',
        17: 'Résidence surveillée',
        19: 'Cuisine américaine',
        20: 'Cuisine séparée',
        21: 'Cuisine équipée',
        22: 'Cuisine aménagée',
        23: 'Salle de bain',
        24: "Salle d'eau",
        25: 'WC indépendant',
        26: 'Terrasse',
        27: 'Balcon',
        28: 'Buanderie',
        29: 'Cellier',
        30: 'Bureau',
        31: 'Meublé',
        32: 'Placards',
        33: 'Jardin',
        34: 'Ascenseur',
        35: 'Chauffe eau',
        36: 'Dressing',
        37: 'Piscine privée',
        38: 'Piscine commune',
        39: 'Climatiseur',
        40: 'Volets électriques',
        42: 'Parking couvert',
        41: 'Garage fermé',
        43: 'Parking',
        44: 'Carport',
    }

    # Map details categories with details from json response
    # category: [details_id, ...]
    extra_details_map = {
        'construction': [1, 3, 4, 5, 6, 7, 8],
        'commodities': [9, 10, 11, 12, 13, 14, 15, 16, 17],
        'pieces': [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
        'equipments': [31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
        'garages': [41, 42, 43, 44]
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
        """Submit search API and get results"""

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
            url = '{}/api/bid/{}'.format(self.start_urls[0], item['id'])
            yield self.make_ajax_request(url, callback=self.parse_item)

            if self.is_test_mode:
                break

    def _get_localization_slug(self, json_data):
        slug = []

        if 'localization' in json_data['realty']:
            localization = json_data['realty']['localization']

            if 'parent' in localization:
                slug.append(slugify(localization['parent']['label']))

            slug.append(slugify(localization['label']))

        return '/'.join(slug)

    def _get_photo_url(self, json_data, size='relativeLargeUrl', idx=0):
        photo_url = ''
        if json_data['realty']['photos']:
            photo_url = '{domain}/media/{image_path}'.format(
                domain=self.start_urls[0],
                image_path=json_data['realty']['photos'][idx][size]
            )
        return photo_url

    def parse_item(self, response):
        """Extract single item from the page"""

        item_loader = ItemLoader(item=BienmelogerCrawlerItem(), response=response)
        meta_item_loader = ItemLoader(item=MetaItem(), response=response)
        id_item_loader = ItemLoader(item=IdItem(), response=response)
        rich_item_loader = ItemLoader(item=RichItem(), response=response)

        json_data = self._parse_json_response(response)

        realty = json_data.get('realty', {})

        realty_type = realty.get('type', {}).get('label', '')

        page_url = '{domain}/{type}/{category}/{realty_type}/{extra_data}/{id}'.format(
            domain=self.start_urls[0],
            type=slugify(json_data.get('type', {}).get('label', '').lower()),
            category=slugify(realty.get('category', {}).get('label', '').lower()),
            realty_type=slugify(realty_type.lower()),
            extra_data=self._get_localization_slug(json_data),
            id=json_data['id']
        )

        item_loader.add_value('objectID', page_url)

        meta_description = textwrap.shorten(json_data['description'], width=158, placeholder=' ...')

        meta_item_loader.add_value('image', self._get_photo_url(json_data, size='relativeMediumUrl'))
        meta_item_loader.add_value('description', meta_description)

        rich_item_loader.add_value('price', json_data.get('formatPrice', ''))
        rich_item_loader.add_value('real_estate_type', json_data.get('type', {}).get('label', ''))
        rich_item_loader.add_value('type', realty.get('category', {}).get('label', ''))
        rich_item_loader.add_value('room_nb', realty_type)
        rich_item_loader.add_value('surface', '%s m2' % realty.get('area', '') if 'area' in realty else '')
        rich_item_loader.add_value('quarter', realty.get('localization', {}).get('label', ''))
        rich_item_loader.add_value('city',
                                   realty.get('localization', {}).get('parent', {}).get('parent', {}).get('label', ''))

        extra_details = collections.defaultdict(list)

        for detail in json_data['realty']['details']:
            details_id = detail['detail']['id']
            if details_id in self.details_map:
                for category_name, detail_ids in self.extra_details_map.items():
                    if details_id in detail_ids:
                        detail_str = '{}: {}'.format(detail['detail']['label'],
                                                     detail.get('value', {}).get('label', ''))
                        extra_details[category_name].append(detail_str)
            else:
                if not self.crawler.stats.get_value(detail['detail']['label'], spider=self):
                    self.crawler.stats.set_value(detail['detail']['label'], {'id': details_id, 'url': page_url},
                                                 spider=self)
                    self.logger.warning("Details '%s': \'%s\' not found in mapping: %s",
                                        details_id, detail['detail']['label'], page_url)

        # format the details into readable format
        for category_name, detail_list in extra_details.items():
            extra_details[category_name] = '\n'.join(detail_list)

        rich_item_loader.add_value(None, extra_details)

        rich_items = rich_item_loader.load_item()

        meta_title = '{real_estate_type} {type} {room_nb} {surface} à {quarter} ({area}) - {price})'.format(
            area=json_data['realty'].get('localization', {}).get('parent', {}).get('label', ''),
            **rich_items
        )

        id_item_loader.add_value('title', meta_title)
        id_item_loader.add_value('domain', 'bienmeloger.nc')
        id_item_loader.add_value('url', page_url)

        item_loader.add_value('id', id_item_loader.load_item())
        item_loader.add_value('meta', meta_item_loader.load_item())
        item_loader.add_value('rich', rich_items)

        yield item_loader.load_item()
