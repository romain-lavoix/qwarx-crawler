# -*- coding: utf-8 -*-

import extruct
import tldextract
from scrapy.loader import ItemLoader
from functools import reduce

from ..items.base import BaseIdItem, BaseMetaItem, BaseQwarxCrawlerItem, BaseRichItem, BaseBoostItem

no_fetch_extract = tldextract.TLDExtract(suffix_list_urls=None)

def get_domain(url):
    domain = reduce(lambda x, y: '{}.{}'.format(x, y), list(filter(lambda x: len(x)  > 0 and x != 'www', no_fetch_extract(url))))

    return domain


def parse(self, response, homepage=False, description_f=None, title_f=None, image_f=None, date_f=None, price_f=None,
          real_estate_type_f=None):
    item_loader = ItemLoader(item=BaseQwarxCrawlerItem(), response=response)
    meta_item_loader = ItemLoader(item=BaseMetaItem(), response=response)
    id_item_loader = ItemLoader(item=BaseIdItem(), response=response)
    rich_item_loader = ItemLoader(item=BaseRichItem(), response=response)
    boost_item_loader = ItemLoader(item=BaseBoostItem(), response=response)
    metadata = None
    url = None

    if response.url.endswith('/'):
        url = response.url[:len(response.url) - 1]
    else:
        url = response.url

    try:
        metadata = extruct.extract(response.body, base_url=url)
    except Exception:
        metadata = None

    jsonld = metadata['json-ld'][0] if metadata is not None and len(metadata['json-ld']) is not 0 else None

    title = None
    if title_f:
        title = title_f(response)
    else:
        title = response.xpath('//meta[@property="og:title"]/@content').extract_first()
        if title is None:
            title = response.xpath('//meta[@property="title"]/@content').extract_first()
            if title is None:
                title = response.xpath("//title/text()").extract_first()

    id_item_loader.add_value('title', title)
    id_item_loader.add_value('domain', get_domain(url))
    id_item_loader.add_value('url', url)

    meta_names = response.xpath("//meta/@name").extract()
    meta_properties = response.xpath("//meta/@property").extract()

    description = None
    if description_f:
        description = description_f(response)
    else:
        if 'description' in meta_names:
            description = response.xpath("//meta[@name='description']/@content").extract_first()
        else:
            if 'og:description' in meta_properties:
                description = response.xpath("//meta[@property='og:description']/@content").extract_first()

    if description is None or len(description) == 0:
        description = title

    meta_item_loader.add_value('description', description)

    image = None
    if metadata is not None and jsonld and 'image' in jsonld:
        json_ld_image = metadata['json-ld'][0]['image']
        if isinstance(json_ld_image, (list,)):
            image = json_ld_image[0]
        elif isinstance(json_ld_image, (dict,)):
            image = json_ld_image['url']
        else:
            image = json_ld_image

    else:
        if image_f:
            image = image_f(response)
        else:
            if 'og:image' in meta_names:
                image = response.xpath("//meta[@name='og:image']/@content").extract_first()
            else:
                if 'og:image' in meta_properties:
                    image = response.xpath("//meta[@property='og:image']/@content").extract_first()

    meta_item_loader.add_value('image', image)

    if 'redirect_urls' in response.meta:
        meta_item_loader.add_value('redirect_urls', response.meta['redirect_urls'])

    date = None
    if date_f:
        date = date_f(response)
    else:
        date = response.xpath('//meta[@property="article:published_time"]/@content').extract_first()
        if date is not None and len(date) == 0 and jsonld is not None and 'datePublished' in jsonld:
            date = jsonld['datePublished']
    rich_item_loader.add_value('date', date)
    meta_item_loader.add_value('date', date)

    price = None
    if price_f:
        price = price_f(response)
    else:
        price = response.xpath('//meta[@property="product:price:amount"]/@content').extract_first()

    rich_item_loader.add_value('price', price)

    longitude = response.xpath('//meta[@property="place:location:longitude"]/@content').extract_first()
    latitude = response.xpath('//meta[@property="place:location:latitude"]/@content').extract_first()

    if longitude and latitude:
        location = {
            "longitude": float(longitude),
            "latitude": float(latitude)
        }
        rich_item_loader.add_value('location', location)

    if real_estate_type_f:
        real_estate_type= real_estate_type_f(response)
        rich_item_loader.add_value('real_estate_type', real_estate_type)

    if homepage or url.endswith(get_domain(url)):
        boost_item_loader.add_value('homepage', True)

    item_loader.add_value('objectID', url)

    item_loader.add_value('id', id_item_loader.load_item())
    item_loader.add_value('meta', meta_item_loader.load_item())
    item_loader.add_value('rich', rich_item_loader.load_item())
    item_loader.add_value('boost', boost_item_loader.load_item())

    yield item_loader.load_item()
