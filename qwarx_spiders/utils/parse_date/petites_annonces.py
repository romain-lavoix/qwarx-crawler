# -*- coding: utf-8 -*-

from ..date import parse_date_generic


def parse_date(datetime_string):
    formatted_datetime_string = datetime_string.replace("Date: ", "")

    return parse_date_generic(formatted_datetime_string)
