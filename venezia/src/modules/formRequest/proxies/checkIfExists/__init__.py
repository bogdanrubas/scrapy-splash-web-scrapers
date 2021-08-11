from scrapy_splash.request import SplashRequest
from .....sql.queries import get_user_agent, get_proxy
from ..catchErrors import _catchErrors
from .....modules.logs.__init__ import Logs
from .....items import Error, DeleteProxy
from twisted.internet.error import TimeoutError


def catchErrors(failure):
    logs = Logs()
    error = Error()
    # ? proxy, ktore zostalo uzyte w tym request:
    usedProxy = {
        'ip': failure.request.meta['ip'],
        'port': failure.request.meta['port']
    }

    # ? Dodaje niedziałające proxy do tablicy deleteProxies
    # ? aby następnie usunąć wszystkie te proxy z
    # ? tablicy proxies
    if failure.check(TimeoutError):
        deleteProxy = DeleteProxy()
        deleteProxy['ip'] = usedProxy['ip']
        deleteProxy['port'] = usedProxy['port']
        yield deleteProxy

    # ? walidacja błędów oraz przypisanie do "error":
    # ? depth, url, meta
    _catchErrors(failure, logs, error)
    for log in logs.addToDatabase():
        yield log
    yield error


def _checkIfExists(self, url, callback, cssSelector, maxTimeout, spider, meta):
    thisDir = (os.path.dirname(
        os.path.realpath(__file__)).replace(os.getcwd(), '')[1:])
    with open(f'{thisDir}/checkIfExists.lua', 'r') as file:
        checkIfExists = file.read()

    proxy = get_proxy(spider)[0]
    ip = proxy[0]
    port = int(proxy[1])
    usedProxy = {
        'ip': ip,
        'port': port
    }

    meta.update(usedProxy)

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
            'timeout': 30,
            'ip': ip,
            'port': port
        },
        meta=meta
    )
