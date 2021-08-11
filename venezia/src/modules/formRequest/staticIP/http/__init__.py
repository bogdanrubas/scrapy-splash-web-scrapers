from scrapy_splash.request import SplashRequest
from .....sql.queries import get_user_agent
from ..catchErrors import _catchErrors
import scrapy
from .....modules.logs.__init__ import Logs
from .....items import Error
import random


def catchErrors(failure):
    logs = Logs()
    error = Error()

    # ? walidacja błędów oraz przypisanie do "error":
    # ? depth, url, meta
    _catchErrors(failure, logs, error)

    yield error
    for log in logs.addToDatabase():
        yield log


def _http(self, url, callback, spider, meta):
    return scrapy.Request(
        url,
        callback=callback,
        errback=catchErrors,
        headers={
            "User-Agent": get_user_agent(spider)[0][0]
        },
        dont_filter=True,
        meta=meta
    )
