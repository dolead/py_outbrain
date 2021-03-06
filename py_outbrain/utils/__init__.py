import re
from datetime import date, datetime
from itertools import chain

import dateutil.parser
from py_outbrain.errors import (BadRequest, NotFound, OutbrainError,
                                ServerError, TooManyRequests, Unauthorized)

ERROR_MAPPING = {
    400: BadRequest,
    401: Unauthorized,
    404: NotFound,
    429: TooManyRequests,
    500: ServerError,
}

DATE_FIELDS = (
    'start_date',
    'end_date',
)


def __cast_as_date(element):
    if isinstance(element, list):
        return [__cast_as_date(e) for e in element]
    return dateutil.parser.parse(element)


def __cast(item):
    if not isinstance(item, dict):
        return item
    new_item = item.copy()
    for key, value in item.items():
        if key in DATE_FIELDS and value:
            new_item[key] = __cast_as_date(value)
        elif isinstance(value, dict):
            new_item[key] = __cast(value)
        else:
            new_item[key] = value
    return new_item


def parse_response(response):
    if not response.ok:
        error = response.text
        if 'application/xml' in response.headers['Content-Type']:
            error = re.search(
                '<error_description>(.*)</error_description>',
                error, re.IGNORECASE)
            if error:
                error = error.group(1)
            else:
                error = response.text
        elif 'application/json' in response.headers['Content-Type']:
            jresp = response.json()
            error = jresp.get('errors') or jresp.get('message')
            error = '\n'.join(chain([error],
                                    jresp.get('validationErrors', [])))

        raise ERROR_MAPPING.get(response.status_code, OutbrainError)(error,
                                                                     response)
    if response.text == '' and response.ok:
        return ''
    return __cast(response.json())


def json_payload_formatter(obj):
    if isinstance(obj, datetime):
        return obj.date().isoformat()
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, set):
        return list(obj)
    return obj
