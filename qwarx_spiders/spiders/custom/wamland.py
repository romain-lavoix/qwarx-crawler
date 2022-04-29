import html2text
import scrapy
from lxml import etree
from lxml import html
from scrapy.loader import ItemLoader

from ..base import BaseSpider
from ...items.wamland import IdItem, MetaItem, RichItem
from ...items.wamland import WamlandItem
from ...utils.parse import get_domain


class WamlandSpider(scrapy.Spider, BaseSpider):
    name = "wamland"

    start_urls = ['https://www.annonces.nc', 'https://automobiles.nc', 'https://embauche.nc', 'https://mobilier.nc/',
                  'https://mode.wamland.nc/', 'https://nautisme.nc/', 'https://piecesauto.nc/',
                  'https://puericulture.nc/']
    allowed_domains = ['annonces.nc', 'automobiles.nc', 'embauche.nc', 'mobilier.nc', 'mode.nc', 'nautisme.nc', 'piecesauto.nc', 'puericulture.nc', 'wamland.nc', 'mode.nc']
    rotate_user_agent = True

    def parse(self, response):

        for category_url in response.xpath('//ul[1]/li//a/@href').extract():
            url = response.urljoin(category_url)
            yield scrapy.Request(url=url, callback=self.parse_category, meta={'deltafetch_key': url})

    def parse_category(self, response):

        category = response.xpath('//div[@id="moteur_recherche_nomCat"]/a/text()').extract_first()
        domain = get_domain(response.url)

        for product_node in response.xpath('//span[contains(@id, "header_annonce_")]'):
            product = {}
            product["Id"] = product_node.xpath('./@id').re_first(r'header_annonce_(\d+)')
            product["Category"] = category
            product["Product_type"] = product_node.xpath('.//table[@class="antnm"]//td[1]/text()').extract_first()
            product["Date"] = product_node.xpath('.//table[@class="antnm"]//td[4]/text()').extract_first()
            product["Title"] = product_node.xpath('string(.//table[@class="antnm"]//td[2])').extract_first()

            #  https://mobilier.nc/a_an.php?g=detail_annonce&id=2958785
            #  https://mobilier.nc/?annonce_rw=2958785
            # "https://{0}/a_an.php?g=detail_annonce&id={1}".format(domain, product["Id"])
            url = "https://{0}/?annonce_rw={1}".format(domain, product["Id"])
            yield scrapy.Request(url=url,
                                 callback=self.parse_product, meta={"product": product, 'deltafetch_key': url})

            # break #DEBUG

        next_page_url = response.xpath('//a[@title="next page"]/@href').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse_category, meta={'deltafetch_key': url})

    def parse_product(self, response):

        product = response.meta["product"]

        item_loader = ItemLoader(item=WamlandItem(), response=response)
        meta_item_loader = ItemLoader(item=MetaItem(), response=response)
        id_item_loader = ItemLoader(item=IdItem(), response=response)
        rich_item_loader = ItemLoader(item=RichItem(), response=response)

        description_node = response.xpath('//div[contains(@id, "detail_")]').extract_first()
        description = None
        if description_node:
            t = html.fromstring(description_node)
            for bad in t.xpath('//b/preceding-sibling::*[1]/following-sibling::*'):
                bad.getparent().remove(bad)
            for bad in t.xpath('//hr/preceding-sibling::*[1]/following-sibling::*'):
                bad.getparent().remove(bad)
            for bad in t.xpath('//i/preceding-sibling::*[1]/following-sibling::*'):
                bad.getparent().remove(bad)

            description_node_converted = etree.tostring(t, pretty_print=True)

            converter = html2text.HTML2Text()
            converter.ignore_links = True
            converter.ignore_images = True

            if description_node_converted:
                description = converter.handle(description_node_converted.decode())

        images = []
        for image_url in response.xpath('//div[@id="gallery"]//li/a/@href').re(r'/(photos\.[^&]+)'):
            image_url = "https://www.annonces.nc/" + image_url

            images.append(image_url)

        id_item_loader.add_value('domain', get_domain(response.url))
        id_item_loader.add_value('url', response.url)
        id_item_loader.add_value('title', product["Title"])

        meta_item_loader.add_value('description', description)
        meta_item_loader.add_value('image', images[0] if len(images) != 0 else None)
        meta_item_loader.add_value('date', product["Date"])

        price = None
        price_response = response.xpath(
            '//div[contains(@id, "detail_")]/b[contains(., "Prix :")]/following-sibling::text()[1]')
        if price_response:
            price = response.xpath(
                '//div[contains(@id, "detail_")]/b[contains(., "Prix :")]/following-sibling::text()[1]')[0].root

        rich_item_loader.add_value('price', price)
        rich_item_loader.add_value('product_category', product["Category"])
        rich_item_loader.add_value('product_type', product["Product_type"])
        rich_item_loader.add_value('images', images[:3])

        item_loader.add_value('objectID', response.url)
        item_loader.add_value('id', id_item_loader.load_item())
        item_loader.add_value('meta', meta_item_loader.load_item())
        item_loader.add_value('rich', rich_item_loader.load_item())

        yield item_loader.load_item()
