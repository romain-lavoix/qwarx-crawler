# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from .errback_httpbin import errback_httpbin
from .parse import parse


class QwarxCrawlSpider(CrawlSpider):
    check_duplicates = True
    rotate_user_agent = True
    rules = (
        Rule(LinkExtractor(
            unique=True,
            deny=(r'.+/calendrier/.+',
                  r'.+iccaldate.+',
                  r'.+/album-photos.+',
                  r'.+/ajaxCalendar.+',
                  r'.+/calendar-created.+',
                  r'.+/calendar-node-field-event.+',
                  r'.+/commande.+',
                  r'.+/events/.+',
                  r'.+/2-accueil.+',
                  r'.+/?add_to_wishlist.+',
                  r'.+/?add-to-cart.+',
                  r'.+/search-notice/.+',
                  r'.+/panier\?.+',
                  r'.+/search.php\?.+',
                  r'.+/en/.+',
                  r'.+date_debut=.+',
                  r'.\?order=.+',
                  ),
        ),
            callback='parse_item',
            follow=True,
        ),
    )

    def parse_item(self, response, description_f=None, title_f=None, image_f=None, price_f=None,
                   real_estate_type_f=None):
        return parse(self, response, description_f=description_f, title_f=title_f, image_f=image_f, price_f=price_f,
                     real_estate_type_f=real_estate_type_f)

    def errback_httpbin(self, failure):
        return errback_httpbin(self, failure)
