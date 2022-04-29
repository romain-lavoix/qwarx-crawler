# -*- coding: utf-8 -*-

import json
import logging
from scrapy.spiders import Spider
from ...services.gsheet import GoogleDriveSheet
from mozscape import Mozscape
import time

from ..base import BaseSpider
import os
import ast
import re
from gspread.exceptions import CellNotFound


logger = logging.getLogger(__name__)
get_chunks = lambda l, n: [l[x: x + n] for x in range(0, len(l), n)]


class CustomCrawlList(Spider, BaseSpider, GoogleDriveSheet):
    """updating custom crawl list in gsheet"""
    name = "update_custom_crawl_list"

    def __init__(self):
        super(GoogleDriveSheet).__init__()

    def start_requests(self):
        spiders = os.listdir('spiders/custom')
        domains = []
        for spider in spiders:
            if spider != '__pycache__':
                with open('spiders/custom/{}'.format(spider), "r") as file:
                    lines = file.read().splitlines()
                    for line in lines:
                        if 'allowed_domains' in line:
                            results = re.findall("\[[\"'].+[\"']]", line)
                            results = ast.literal_eval(line.strip().replace("allowed_domains = ", ""))
                            domains.append(results)
        flat_domains = [item for sublist in domains for item in sublist]

        worksheet_nc = self.get_worksheet('DOMAINS_NC')
        worksheet_ext = self.get_worksheet('DOMAINS_EXT')
        for domain in flat_domains:
            worksheet = worksheet_nc if domain.endswith('.nc') else worksheet_ext
            cell = None
            try:
                cell = worksheet.find(domain)
                if worksheet.cell(cell.row, 4).value == 'FALSE':
                    continue
            except CellNotFound:
                logger.warning('cannot find {}'.format(domain))
                continue
            # we find the domain row position, and set crawl_activated to FALSE
            worksheet.update_cell(cell.row, 4, 'FALSE')
            logger.info('deactivating broad crawl on {}'.format(domain))
