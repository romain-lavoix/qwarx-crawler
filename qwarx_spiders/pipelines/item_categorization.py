import ast
import json
import logging
from algoliasearch import algoliasearch

from scrapy.utils.serialize import ScrapyJSONEncoder

from ..services.aws import AWSBase
from ..services.gsheet import GoogleDriveSheet
from ..utils.cache import cache
algolia_client = algoliasearch.Client("5NXUF7YDRN", 'ce00544c03c7016cbf0e45e976d8a6d2')
index = algolia_client.init_index('qwarx.nc')
logger = logging.getLogger(__name__)

class ItemCategorizationPipeline(AWSBase, GoogleDriveSheet):
    def __init__(self, settings):
        self.settings = settings
        self.s3 = None
        self.domains_infos = {}
        self.queue_items = []
        self.queue_size = self.settings.getint('AWS_SQS_QUEUE_CHUNK_SIZE', 200)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        self.s3 = self.get_aws_s3()
        self.domains_infos = self.get_domains_infos()

    def close_spider(self, spider):
        # When we close the spider we need to make sure all the items
        # from queue are sent
        if not self.is_queue_empty:
            self.send_items_from_queue_to_sqs()

    def process_item(self, item, spider):
        if self.is_queue_full:
            self.send_items_from_queue_to_sqs()
        else:
            item = self.categorize_item(item, spider)
            self.queue_items.append(item)

        return item

    @property
    def is_queue_full(self):
        return len(self.queue_items) == self.queue_size

    @property
    def is_queue_empty(self):
        return not bool(len(self.queue_items))

    def reset_queue(self):
        self.queue_items = []

    @cache.memoize(name='domains_infos', typed=True, expire=60 * 60, tag='domain')
    def get_domains_infos(self):
        """Get domains authorities from gsheet."""

        logger.info("Get Domains Infos from Qwarx_DB...")

        domains_infos = self.gsheet_get_domains_infos()

        logger.info("Get Domains Infos from Qwarx_DB... OK")

        return domains_infos

    def categorize_item(self, item, spider):
        """Add extra categories and boost option for algolia DB"""

        # first let's set up the boost scores
        domain = item['id']['domain']
        item.setdefault('boost', {})
        if domain in self.domains_infos:
            domain_info = self.domains_infos[domain]
            item['category'] = domain_info.get('category', 'no-domain')
            if item['category'] == 'classifieds' and 'immobilier' in item['objectID']:
                item['category'] = 'realestate'
            item['boost']['domain_authority'] = domain_info.get('authority', 0)


        item['spider_name'] = spider.name


        item['boost']['image'] = 'image' in item['meta']
        item['boost']['meta_description'] = 'description' in item['meta']

        return item

    def send_items_from_queue_to_sqs(self):
        """Send a chunk of items to Algolia """

        logger.info("Send chunk of '%s' items to SQS Queue", len(self.queue_items))

        items = list()
        for item in self.queue_items:
            items.append(item._values)

        sqs = self.get_aws_sqs()

        sqs_queue = sqs.get_queue_by_name(QueueName=self.settings.get('AWS_SQS_QUEUE_NAME'))

        response = sqs_queue.send_message(
            MessageBody=json.dumps(items, cls=ScrapyJSONEncoder)
        )

        # res = index.add_objects(items)
        # index.wait_task(res["taskID"])
        # if 'message' in res:
        #     logger.error(res['message'])
        # if 'objectIDs' in res:
        #     logger.info("Items inserted : %s", res['objectIDs'])

        logger.info("Send to SQS, response: %s", response)


        self.reset_queue()

    def __getstate__(self):
        # To properly make cache work we need to exclude from pickle s3 object
        state = self.__dict__.copy()

        del state['s3']

        return state
