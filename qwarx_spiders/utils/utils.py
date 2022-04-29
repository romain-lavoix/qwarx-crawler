# -*- coding: utf-8 -*-

import datetime
import re
import time
from scrapy.loader.processors import TakeFirst


class TakeFirstAndEmpty(TakeFirst):
    def __call__(self, values):
        for value in values:
            if value is not None:
                return value


def str_strip(s):
    return s.strip() or None


def str_strip_allow_empty(s):
    return s.strip()


def limit_description(s):
    return s if len(s) < 270 else '{}...'.format(s[:270])


def output_description(lines):
    output = ''
    for line in lines:
        if len(output) == 0:
            output = line
        else:
            output = '{0} | {1}'.format(output, line)

    output = limit_description(output)
    return output


def limit_title(s):
    return s if len(s) < 70 else '{}...'.format(s[:70])


def parse_date(date):
    try:
        date_human = date[:10]
        parsed_date = time.mktime(datetime.datetime.strptime(date_human, "%Y-%m-%d").timetuple())
    except:
        parsed_date = None
    return parsed_date


def parse_date_human(date):
    date_human = date[:10]
    return date_human


def base64_check(url):
    if 'base64' in url:
        return None
    else:
        return url


def clean_url(url):
    if url.endswith('/'):
        return url[:len(url) - 1]
    else:
        return url


def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html) if raw_html is not None else ''
    return cleantext


def clear(value):
    if value is None:
        value = ""

    if isinstance(value, str):
        value = value.strip()
        value = value.replace(u'\xa0', u' ')
        value = str(value)

    if isinstance(value, str):
        value = value.strip()
        value = value.replace(u'\xa0', u' ')

    return value


def remove_newlines(value):
    if value is None:
        value = ""

    if isinstance(value, str):
        value = re.sub(r'[\r\n]', " ", value)
        value = re.sub(r'\s+', " ", value)
        value = re.sub(r'^\s+|\s+$', "", value)
        value = str(value)

    if isinstance(value, str):
        value = value.replace(u'\xa0', u' ')
        value = re.sub(r'[\r\n]', " ", value)
        value = re.sub(r'\s+', " ", value)
        value = re.sub(r'^\s+|\s+$', "", value)

    return value


def clean_price(value):
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        value = value.replace(' ', '')
        millions = False
        if 'U' in value:
            millions = True
        value = value.replace('XPF', '').replace('CFP', '').replace('F', '').replace('U', '').replace(',', '.')
        try:
            float(value)
        except ValueError:
            return None
        price = float(value)
        price = price * 1000000 if millions else price
        return int(price)
    return None
