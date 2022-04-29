# -*- coding: utf-8 -*-
import datetime
import time

import dateparser
from pytz import timezone


def parse_date_generic(datetime_string, languages=('fr',), locales=('fr',)):
    dt_ad = dateparser.parse(datetime_string, languages=languages, locales=locales,
                             settings={'TIMEZONE': 'Pacific/Noumea', 'RETURN_AS_TIMEZONE_AWARE': True})
    if dt_ad is None:
        return 0
    dt_ad = dt_ad.date()

    dt_now = datetime.datetime.now(timezone('Pacific/Noumea')).date()

    if dt_ad > dt_now:
        dt_ad = dt_ad.replace(year=dt_now.year - 1)

    timestamp_ad = time.mktime(dt_ad.timetuple())

    return timestamp_ad
