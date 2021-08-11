from scrapy_splash.request import SplashRequest
from ..catchErrors import _catchErrors
from .....modules.logs.__init__ import Logs
from .....items import Error


def catchErrors(failure):
    logs = Logs()
    error = Error()

    # ? walidacja błędów oraz przypisanie do "error":
    # ? depth, url, meta
    _catchErrors(failure, logs, error)

    yield error
    for log in logs.addToDatabase():
        yield log


def _executeJS(self, url, callback, luaScript, spider, meta):
    return SplashRequest(
        url,
        callback=callback,
        errback=catchErrors,
        dont_filter=True,
        endpoint='execute',
        args={
            'lua_source': luaScript,
            'ua': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'
        },
        meta=meta,
        cache_args=['lua_source'],
        headers={'X-My-Header': 'value'},
    )
