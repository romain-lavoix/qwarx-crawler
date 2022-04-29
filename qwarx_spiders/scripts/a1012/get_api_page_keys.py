# -*- coding: utf-8 -*-

import concurrent.futures
import json
import logging
import string
import time
from collections import defaultdict

import furl
from selenium.webdriver import PhantomJS
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

API_PAGE_SIZE = 1900
API_PAGE_KEYS_FILE = 'api_page_keys.py'
MAX_WORKERS = 20

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
}

COMMUNE_LIST = [
    {"id": 98812, "libelle": "BOULOUPARIS"}, {"id": 98814, "libelle": "OUVEA"},
    {"id": 98827, "libelle": "POYA"}, {"id": 98831, "libelle": "TOUHO"}, {"id": 98813, "libelle": "CANALA"},
    {"id": 98835, "libelle": "DUMBEA"}, {"id": 98815, "libelle": "HIENGHENE"},
    {"id": 98817, "libelle": "KAALA GOMEN"}, {"id": 98859, "libelle": "KONE"},
    {"id": 98889, "libelle": "PAITA"}, {"id": 98822, "libelle": "POINDIMIE"},
    {"id": 98825, "libelle": "POUEMBOUT"}, {"id": 98828, "libelle": "MARE"},
    {"id": 98882, "libelle": "SARRAMEA"}, {"id": 98819, "libelle": "MOINDOU"},
    {"id": 98829, "libelle": "THIO"}, {"id": 98832, "libelle": "ILE DES PINS"},
    {"id": 98820, "libelle": "LIFOU"}, {"id": 98870, "libelle": "BOURAIL"},
    {"id": 98880, "libelle": "LA FOA"}, {"id": 98881, "libelle": "FARINO"},
    {"id": 98800, "libelle": "NOUMEA"}, {"id": 98821, "libelle": "OUEGOA"},
    {"id": 98824, "libelle": "POUEBO"}, {"id": 98833, "libelle": "VOH"}, {"id": 98834, "libelle": "YATE"},
    {"id": 98811, "libelle": "BELEP"}, {"id": 98816, "libelle": "HOUAILOU"},
    {"id": 98818, "libelle": "KOUAOUA"}, {"id": 98850, "libelle": "KOUMAC"},
    {"id": 98809, "libelle": "MONT DORE"}, {"id": 98823, "libelle": "PONERIHOUEN"},
    {"id": 98826, "libelle": "POUM"}
]

SEARCH_LETTERS = list(string.ascii_lowercase)

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)


class APIKeysCrawler(object):
    def __init__(self):
        pass

    def logd(self, msg):
        logging.debug(msg)

    def loge(self, msg):
        logging.error(msg)

    def init_web_driver(self):
        for key, value in HEADERS.items():
            DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value

        DesiredCapabilities.PHANTOMJS[
            'phantomjs.page.settings.userAgent'] = HEADERS['User-Agent']

        service_args = [
            '--ignore-ssl-errors=true'
        ]

        return PhantomJS(service_args=service_args)

    def get_header(self, driver, url_part, header_name, header_type='request'):
        entries = json.loads(driver.get_log('har')[0]['message'])['log']['entries']

        for entry in entries:
            if url_part in entry['request']['url']:
                for header in entry[header_type]['headers']:
                    if header['name'] in (header_name,):
                        return header['value']

    def get_results_from_search(self, url_type, api_type, commune_name, search_query, size):
        driver = self.init_web_driver()

        api_url = f'api/v1/{api_type}'

        max_pages = None
        page = 1
        total_items = 0
        sleep_time = 5

        items = defaultdict(dict)

        items[search_query] = {
            'pages': []
        }

        while max_pages is None or page <= max_pages:
            base_msg = "[%s] commune_name='%s', search_query='%s', page='%s'" % (
                api_type, commune_name, search_query, page)
            self.logd('%s start...' % base_msg)

            url = 'https://www.1012.nc/{url_type}/recherche?quiQuoi={search_query}&commune={commune_name}&isRubric=false&page={page}&size={size}&type=ALL'.format(
                url_type=url_type,
                page=page,
                size=size,
                search_query=search_query,
                commune_name=commune_name
            )
            driver.get(url)
            time.sleep(sleep_time)

            if max_pages is None:
                link_header = self.get_header(driver, api_url, 'Link', header_type='response')
                if not link_header:
                    self.logd('%s: Link header not found, try again' % base_msg)
                    break
                fu = furl.furl(
                    list(filter(lambda x: 'rel="last"' in x, link_header.split(',')))[0])

                # Because here page is zero indexed
                max_pages = int(fu.args['page']) + 1
                self.logd('%s: Found %s pages' % (base_msg, max_pages))

            if not items[search_query].get('total'):
                total_items = int(self.get_header(driver, api_url, 'X-Total-Count', header_type='response'))
                self.logd('%s: Found %s total_items' % (base_msg, total_items))

            key_header = self.get_header(driver, api_url, 'X-RS')
            if key_header:
                items[search_query]['pages'].append(
                    {'page': page, 'key': key_header, 'size': size}
                )
                self.logd("%s: key_header='%s'" % (base_msg, key_header))
                page += 1
            else:
                self.logd("%s: No key header found, try again" % (base_msg,))

            if total_items > size:
                total_items -= size

                if total_items < size:
                    size = total_items

        driver.quit()

        return items

    def get_all_search_keys(self):
        url_composer = {
            'professionnels': {
                'api_type': 'pagesjaunes',
                'size': API_PAGE_SIZE,
                'enabled': True
            },
            'particuliers': {
                'api_type': 'pagesblanches',
                'size': API_PAGE_SIZE,
                'enabled': True
            }
        }

        data = defaultdict(dict)

        for url_type, url_params in url_composer.items():
            if not url_params['enabled']:
                self.logd("Skip '%s'" % url_type)
                continue
            api_type = url_params['api_type']

            data[api_type]['url_type'] = url_type
            data[api_type]['items'] = defaultdict(dict)

            with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = {}

                for commune in COMMUNE_LIST:
                    commune_name = commune['libelle']

                    for search_query in SEARCH_LETTERS:
                        submited_future = executor.submit(self.get_results_from_search, url_type, api_type,
                                                          commune_name,
                                                          search_query, url_params['size'])

                        futures[submited_future] = commune_name

                for future in concurrent.futures.as_completed(futures):
                    commune_name = futures[future]

                    try:
                        data[api_type]['items'][commune_name].update(future.result())
                    except Exception as exc:
                        self.loge(exc)
                        import traceback
                        self.loge(traceback.format_exc())

        return data

    def save_data(self, data):
        file_path = '%s' % API_PAGE_KEYS_FILE
        with open(file_path, 'w') as f:
            f.write('API_PAGE_KEYS = %s' % json.dumps(data, indent=4, ensure_ascii=False))

        self.logd("Saved to: '%s'" % file_path)

    def run(self):
        self.logd("START")
        self.save_data(self.get_all_search_keys())
        self.logd("END")


if __name__ == '__main__':
    APIKeysCrawler().run()
