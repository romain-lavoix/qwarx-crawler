# -*- coding: utf-8 -*-

import dateparser
import re


def parse_date(datetime_string, lang='fr'):
    dt = ''

    re_datetime = re.search('.+?(\d+.+\d+).+', datetime_string)
    if re_datetime:
        dt = dateparser.parse(re_datetime.group(1), languages=[lang], locales=[lang])

    return dt
