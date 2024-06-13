import os
from datetime import datetime as dt
from pytz import timezone

tz_name = 'UTC' if os.getenv('TZ_NAME') is None else os.getenv('TZ_NAME')

tz = timezone(tz_name)


def getNow():
    return tz.localize(dt.now())


def getDictKey(dict_obj, key, ignore_key_error=True):
    try:
        return dict_obj[key]

    except KeyError:
        if ignore_key_error:
            return None

        else:
            raise
