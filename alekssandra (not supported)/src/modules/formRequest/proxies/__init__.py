import os
from ....modules.logs.__init__ import Logs
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from scrapy_splash.request import SplashRequest
from .waitForSelector.__init__ import _waitForSelector
from .checkIfExists.__init__ import _checkIfExists
from .waitForFullPage.__init__ import _waitForFullPage
from .executeJS.__init__ import _executeJS
from .http.__init__ import _http
from ....items import Error
import random
import scrapy
import json

# ? http(self, url, callback, spider, meta)
# ? zwykły request, najszybszy ze wszystkich

# ? waitForSelector(self, url, callback, cssSelector, spider, meta)
# ? gdy MAMY PEWNOŚĆ, ze cssSelector pojawi się na stronie

# ? executeJS(self, url, callback, luaScript, spider, meta)
# ? gdy chcemy uruchomić jakiś JS

# ? waitForFullPage(self, url, callback, spider, meta)
# ? gdy potrzebujemy całej strony
# ? (default delay: 5s)

# ? checkIfExists(self, url, callback, cssSelector, maxTimeout, spider, meta)
# ? gdy chcemy sprawdzić czy dany element pojawił się na stronie
# ? maxTimeout - maksymalny czas oczekiwania na element
# ? response.data['isExists'] = true or false


class FormRequest(object):
    def checkIfExists(self, url, callback, cssSelector, maxTimeout, spider, meta):
        return _checkIfExists(self, url, callback, cssSelector, maxTimeout, spider, meta)

    def waitForFullPage(self, url, callback, spider, meta):
        return _waitForFullPage(self, url, callback, spider, meta)

    def executeJS(self, url, callback, luaScript, spider, meta):
        return _executeJS(self, url, callback, luaScript, spider, meta)

    def waitForSelector(self, url, callback, cssSelector, spider, meta):
        return _waitForSelector(self, url, callback, cssSelector, spider, meta)

    def http(self, url, callback, spider, meta):
        return _http(self, url, callback, spider, meta)
