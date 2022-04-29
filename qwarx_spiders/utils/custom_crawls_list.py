# -*- coding: utf-8 -*-

import ast
import os

import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import pkgutil

def auth(self):
    drive_access = json.loads(pkgutil.get_data("qwarx_spiders", "/resources/drive_access.json"))
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(drive_access, self.SCOPE)
    return gspread.authorize(credentials)

def get_worksheet(self, sheet_name):
    sheet_key = self.settings.get('QWARX_DB_GSHEET_KEY')
    gc = self.auth()
    sh = gc.open_by_key(sheet_key)
    return sh.worksheet(sheet_name)

def get_custom_crawl_domains(self):
    spiders = os.listdir('qwarx_spiders/spiders/custom')
    domains = []
    for spider in spiders:
        if spider != '__pycache__':
            with open('qwarx_spiders/spiders/custom/{}'.format(spider), "r") as file:
                lines = file.read().splitlines()
                for line in lines:
                    if 'allowed_domains' in line:
                        results = re.findall("\[[\"'].+[\"']]", line)
                        results = ast.literal_eval(line.strip().replace("allowed_domains = ", ""))
                        print(results)
                        domains.append(results)
    flat_domains = [item for sublist in domains for item in sublist]

    with open('qwarx_spiders/results/custom_crawl_domains.txt', 'w') as file:
        for domain in flat_domains:
            file.write('{}\n'.format(domain))
