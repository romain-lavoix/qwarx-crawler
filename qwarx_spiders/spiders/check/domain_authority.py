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


class DomainAuthority(Spider, BaseSpider, GoogleDriveSheet, AlgoliaSearchBase):
    """updating moz scores in gsheet"""
    name = "domain_authority"

    def __init__(self):
        super(GoogleDriveSheet).__init__()

    def start_requests(self):
        domains = []
        for row in self.get_sheet_rows('DOMAINS_EXT'):
            domains.append(row[0])
        domains.pop(0)
        domain_authority_cell_list = self.get_domain_authority_cell_list('DOMAINS_EXT')
        chunks = get_chunks(domains, 10)
        logger.info('starting moz analysis on {} domains'.format(len(domains)))
        client = Mozscape('mozscape-73767a2838', 'f45d344dde4cf860e001217d3be9e8f1')

        i = 0
        chunk_count = 0
        worksheet = self.get_worksheet('DOMAINS_EXT')
        logger.info('gsheet auth')
        for chunk in chunks:
            metrics = client.urlMetrics(chunk, Mozscape.UMCols.domainAuthority)
            chunk_count += 1
            logger.info('progress {}/{}'.format(chunk_count, len(chunks)))
            j = 0
            domain_authority_sub_cell_list = list()
            if chunk_count % 50 == 0:
                logger.info('gsheet auth refresh')
                worksheet = self.get_worksheet('DOMAINS_EXT')
            for domain in chunk:
                metric = metrics[j]
                domain_authority_cell = domain_authority_cell_list[i]
                domain_authority_cell.value = metric['pda']
                domain_authority_sub_cell_list.append(domain_authority_cell)
                i += 1
                j += 1

            worksheet.update_cells(domain_authority_sub_cell_list)
            time.sleep(10)
