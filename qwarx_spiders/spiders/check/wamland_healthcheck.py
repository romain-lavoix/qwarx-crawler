import html2text
import scrapy
from lxml import etree
from lxml import html

from ..base import BaseSpider
from ...services.algolia import AlgoliaSearchBase
import logging

logger = logging.getLogger(__name__)


class WamlandHealthCheckSpider(scrapy.Spider, BaseSpider, AlgoliaSearchBase):
    name = "wamland_healthcheck"
    bucket_size = 100

    rotate_user_agent = True

    def __init__(self, *args, **kwargs):
        super(WamlandHealthCheckSpider, self).__init__(WamlandHealthCheckSpider, *args, **kwargs)
        self.urls_to_delete = []
        self.nb_urls_to_delete = 0
        self.nb_urls = 0
        self.nb_urls_processed = 0

    def start_requests(self):
        items_index = self.get_algolia_index(self.settings.get('ALGOLIA_SEARCH_INDEX'))
        items = items_index.browse_all({"filters": 'spider_name:wamland'})
        urls = []
        for item in items:
            urls.append(item['objectID'])

        self.nb_urls = len(urls)
        for url in urls:
            self.nb_urls_processed = self.nb_urls_processed + 1
            yield scrapy.Request(url, callback=self.verify, dont_filter=True)

    def verify(self, response):

        description_node = response.xpath('//div[contains(@id, "detail_")]').extract_first()
        if description_node is None:

            self.nb_urls_to_delete = self.nb_urls_to_delete + 1
            logger.info('adding {} to the list of urls to delete'.format(response.url))
            logger.info('404 count {} / {} urls processed / {} urls total'.format(self.nb_urls_to_delete,
                                                                                  self.nb_urls_processed,
                                                                                  self.nb_urls))
            self.urls_to_delete.append(response.url)

        if len(self.urls_to_delete) == self.bucket_size or (
                self.nb_urls != 0 and (self.nb_urls == self.nb_urls_processed)):
            logger.info('deleting from Algolia : {}'.format(', '.join(map(str, self.urls_to_delete))))
            algolia_index = self.get_algolia_index()
            algolia_index.delete_objects(self.urls_to_delete)
            self.urls_to_delete.clear()
