
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from ..clearRequestMeta import clearRequestMeta
import json


def addLog(logs, url, type):
    logs.add(
        'ERROR',
        'catchErrors' + ' [' + type + ']',
        type,
        url
    )


def _catchErrors(failure, logs, error):
    url = ''
    request = failure.request

    error['depth'] = request.meta['depth']
    if 'splash' in request.meta:
        url = request.meta['splash']['args']['url']
    else:
        url = request.url
    error['url'] = url
    clearRequestMeta(request.meta)
    error['meta'] = json.dumps(request.meta)

    if failure.check(HttpError):
        addLog(logs, url, 'HttpError')

    elif failure.check(ConnectionRefusedError):
        addLog(logs, url, 'ConnectionRefusedError')

    elif failure.check(DNSLookupError):
        addLog(logs, url, 'DNSLookupError')

    elif failure.check(TimeoutError):
        addLog(logs, url, 'TimeoutError')

    elif failure.check(TCPTimedOutError):
        addLog(logs, url, 'TCPTimedOutError')
