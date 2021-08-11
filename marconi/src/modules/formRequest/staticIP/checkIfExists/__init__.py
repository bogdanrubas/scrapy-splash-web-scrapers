from scrapy_splash.request import SplashRequest
from .....sql.queries import get_user_agent
from ..catchErrors import _catchErrors
from .....modules.logs.__init__ import Logs
from .....items import Error
import os


def catchErrors(self, failure):
    logs = Logs()
    error = Error()

    # ? walidacja błędów oraz przypisanie do "error":
    # ? depth, url, meta
    _catchErrors(failure, logs, error)

    yield error
    for log in logs.addToDatabase():
        yield log


def _checkIfExists(self, url, callback, cssSelector, maxTimeout, spider, meta):
    thisDir = (os.path.dirname(
        os.path.realpath(__file__)).replace(os.getcwd(), '')[1:]).replace('/private', 'private')
    with open(f'{thisDir}/checkIfExists.lua', 'r') as file:
        checkIfExists = file.read()

    return SplashRequest(
        url,
        callback=callback,
        errback=self.catchErrors,
        dont_filter=True,
        endpoint='execute',
        args={
            'lua_source': checkIfExists,
            'ua': get_user_agent(spider)[0][0],
            'cssSelector': cssSelector,
            'maxTimeout': maxTimeout,
            'timeout': 60
        },
        meta=meta
    )
