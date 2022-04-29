import logging

from ..services.algolia import AlgoliaSearchBase

logger = logging.getLogger(__name__)


class ResetSpiderDataPipeline(AlgoliaSearchBase):
    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        reset_spider_data = getattr(spider, 'algolia_reset_spider_data',
                                    self.settings.getbool('ALGOLIA_RESET_SPIDER_DATA'))

        reset_spider_data = eval(str(reset_spider_data))

        if reset_spider_data:
            spider_name = spider.name
            logger.info("[spider=%s] Reset Algolia data...", spider_name)

            search_index = self.get_algolia_index()
            res = search_index.delete_by({'filters': 'spider_name:%s' % spider_name})
            search_index.wait_task(res["taskID"])

            logger.info("[spider=%s] Reset Algolia -> OK", spider_name)
