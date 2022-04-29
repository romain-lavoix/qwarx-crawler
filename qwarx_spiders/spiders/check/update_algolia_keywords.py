# -*- coding: utf-8 -*-

import json
import logging
from scrapy.spiders import Spider
from ...services.gsheet import GoogleDriveSheet
from ...services.algolia import AlgoliaSearchBase
from mozscape import Mozscape
import time

from ..base import BaseSpider

logger = logging.getLogger(__name__)
get_chunks = lambda l, n: [l[x: x + n] for x in range(0, len(l), n)]


class UpdateAlgoliaKeywords(Spider, BaseSpider, GoogleDriveSheet, AlgoliaSearchBase):
    """updating algolia keywords from gsheet to algolia"""
    name = "update_algolia_keywords"

    def __init__(self):
        super(GoogleDriveSheet).__init__()

    def start_requests(self):
        infos = []
        for row in self.get_sheet_rows('ALGOLIA_KEYWORDS'):
            infos.append({
                'url': row[0],
                'boost_type' : row[1],
                'value' : row[2],
                'start_date': 0,
                'end_date': 0
            })
        infos.pop(0)

