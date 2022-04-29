import json
import pkgutil

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from mozscape import Mozscape
import time


class GoogleDriveSheet(object):
    SCOPE = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]

    def __init__(self):
        pass

    def auth(self):
        drive_access = json.loads(pkgutil.get_data("qwarx_spiders", "/resources/drive_access.json"))
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(drive_access, self.SCOPE)
        return gspread.authorize(credentials)

    def get_sheet_rows(self, sheet_name, sheet_key=None):
        feeds = self.get_worksheet(sheet_name)
        rows = feeds.get_all_values()
        rows.pop(0)
        return rows

    def get_worksheet(self, sheet_name):
        sheet_key = self.settings.get('QWARX_DB_GSHEET_KEY')
        gc = self.auth()
        sh = gc.open_by_key(sheet_key)
        return sh.worksheet(sheet_name)

    def get_domain_authority_cell_list(self, sheet_name):
        gc = self.auth()
        sh = gc.open_by_key(self.settings.get('QWARX_DB_GSHEET_KEY'))
        worksheet = sh.worksheet(sheet_name)
        nb_domains = len(worksheet.get_all_values()) - 1

        get_domain_authority_cell_list = worksheet.range('E2:E{}'.format(nb_domains))
        return get_domain_authority_cell_list

    def gsheet_get_domains_infos(self):
        domains_infos = {}
        for sheet_name in ['DOMAINS_EXT', 'DOMAINS_NC']:
            for row in self.get_sheet_rows(sheet_name):
                domain_name, authority, category, activated = row[0], row[4], row[2], row[3]
                domains_infos[domain_name] = {
                    'authority': authority,
                    'category': category,
                    'activated': activated


                }
        return domains_infos

    def update_nc_domains(self, domains):
        worksheet = self.get_worksheet('DOMAINS_NC')
        rows = worksheet.get_all_values()
        rows.pop(0)
        idx = len(rows) + 1
        client = Mozscape('mozscape-73767a2838', 'f45d344dde4cf860e001217d3be9e8f1')

        g_domains = set()
        for row in rows:
            g_domains.add(row[0])

        for domain in domains:
            if domain not in g_domains:
                idx += 1
                cell_list = worksheet.range('A{idx}:E{idx}'.format(idx=idx))
                metrics = client.urlMetrics([domain], Mozscape.UMCols.domainAuthority)
                cell_list[0].value = domain
                cell_list[1].value = 'not_defined'
                cell_list[2].value = 'other'
                # by default, we don't automatically crawl a domain, it needs to be verified manually
                cell_list[3].value = 'FALSE'
                cell_list[4].value = metrics[0]['pda']
                worksheet.update_cells(cell_list)
                time.sleep(9)
