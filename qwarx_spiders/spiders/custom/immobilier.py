# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader import ItemLoader
from scrapy.utils.url import parse_url

from ..base import BaseSpider
from ...items.immobilier import IdItem, MetaItem, RichItem
from ...items.immobilier import ImmobilierCrawlerItem


class ImmobilierSpider(scrapy.Spider, BaseSpider):
    name = 'immobilier'
    allowed_domains = ['immobilier.nc']
    start_urls = ['https://immobilier.nc/']

    custom_settings = {
        'DOWNLOAD_TIMEOUT': 120
    }

    PAGINATOR_ITEM_SIZE = 400

    def ajax_request(self, url, response, callback=None, method='GET', formdata=None, **kwargs):
        """Make an ajax request by setting proper headers"""

        headers = {'X-Requested-With': 'XMLHttpRequest'}
        if method == 'GET':
            yield response.follow(url, headers=headers, callback=callback, **kwargs)
        else:
            yield scrapy.FormRequest(url, headers=headers, callback=callback, formdata=formdata, dont_filter=True,
                                     **kwargs)

    def parse(self, response):
        """Initial request to follow all the categories from the main page. We are making an ajax request
        for this in order to mimic how they implemented it from the browser"""

        formdata = {
            "section": "offres_location",
            "bien": "",
            "type": "",
            "prix_location": "",
            "prix_vente": "",
            "pays": "nc",
            "ville": "",
            "quartier": "",
            "par_page": "{}".format(self.PAGINATOR_ITEM_SIZE),
            "orderBy": "",
            "orderDirection": "DESC",
            "moteurRecherche_option": ""
        }

        sections = response.xpath('//select[@id="section"]/descendant-or-self::option/@value').extract()

        sections = list(filter(None, sections))

        for section in sections:
            formdata['section'] = section
            for category_name in response.xpath('//tr[@class="lien_accueil"]/td[last()]/text()').extract():
                category_name = category_name.strip()
                if category_name:
                    formdata['bien'] = category_name
                    meta = {
                        'section': section
                    }
                    yield from self.ajax_request('https://immobilier.nc/immo_offres.php', response, method='POST',
                                                 formdata=formdata, callback=self.parse_category_page,
                                                 meta=meta)
                    if self.is_test_mode:
                        break
            if self.is_test_mode:
                break

    def parse_category_page(self, response):
        """Parse paginator and make sure we follow all the pages. """

        yield from self.parse_category_items(response)

        for page_el in response.xpath('//table[@id="id_topSite"][1]/descendant-or-self::a[@class="goPager"]'):
            try:
                int(page_el.xpath('text()').extract_first())
                next_page_url = page_el.xpath('@href').extract_first()
                meta = {
                    'section': response.meta['section']
                }
                yield from self.ajax_request(next_page_url, response, callback=self.parse_category_items, meta=meta)
            except TypeError:
                pass

    def parse_category_items(self, response):
        """Now we have a table with all the item we need to follow. We extract some details from the general table
        and other from the details page"""

        section1, section2 = response.meta['section'].split('_')

        for item_el in response.xpath('//tr[@data-pushstat_url]'):
            item_url = item_el.xpath('@href').extract_first()

            page_url = response.urljoin(item_el.xpath('@data-pushstat_url').extract_first())
            rich_item_loader = ItemLoader(item=RichItem(), response=response, selector=item_el)

            rich_item_loader.add_value('section1', section1)
            rich_item_loader.add_value('real_estate_type', section2)
            rich_item_loader.add_xpath('bien', 'td[5]/text()')
            rich_item_loader.add_xpath('type', 'td[6]/text()')
            rich_item_loader.add_xpath('ville', 'td[7]/text()')
            rich_item_loader.add_xpath('quartier', 'td[8]/text()')
            rich_item_loader.add_xpath('price', 'td[9]/text()')
            rich_item_loader.add_xpath('date', 'td[10]/text()')

            item_url = item_url.replace('menu_detail_offre.php', 'detail_offre.php')
            url = item_url + '&view=>'
            yield from self.ajax_request(url, response, callback=self.parse_meta_details,
                                         meta={'rich_item': rich_item_loader.load_item(), 'page_url': page_url})
            if self.is_test_mode:
                break

    def parse_meta_details(self, response):
        """Parse more details about the meta item"""

        page_details_el = response.xpath('//div[@id="page_detail_offre"]')
        rich_item = response.meta['rich_item']
        page_url = response.meta['page_url']

        meta_item_loader = ItemLoader(item=MetaItem(), response=response, selector=page_details_el)
        meta_item_loader.add_xpath('description', 'p[3]/descendant-or-self::text()')

        yield scrapy.Request(page_url, callback=self.parse_item_details,
                             meta={'meta_item': meta_item_loader.load_item(), 'rich_item': rich_item})

    def parse_item_details(self, response):
        """General information required to run on scrapping hub"""

        rich_item = response.meta['rich_item']
        meta_item = response.meta['meta_item']
        page_url = response.url

        item_loader = ItemLoader(item=ImmobilierCrawlerItem(), response=response)

        id_item_loader = ItemLoader(item=IdItem(), response=response)
        meta_item_loader = ItemLoader(item=meta_item, response=response)
        rich_item_loader = ItemLoader(item=rich_item, response=response)

        item_loader.add_value('objectID', page_url)

        title = ' '.join(
            filter(None, (rich_item.get(f) for f in ('section1', 'section2', 'bien',
                                                     'type', 'ville', 'quartier'))))

        id_item_loader.add_value('title', title)
        id_item_loader.add_value('domain', parse_url(response.url).hostname)
        id_item_loader.add_value('url', page_url)

        meta_item_loader.add_xpath('image', '//meta[@property="og:image"]/@content')
        meta_item_loader.add_xpath('date', '//meta[@property="og:image"]/@content')


        item_loader.add_value('id', id_item_loader.load_item())
        item_loader.add_value('meta', meta_item_loader.load_item())
        item_loader.add_value('rich', rich_item_loader.load_item())

        yield item_loader.load_item()
