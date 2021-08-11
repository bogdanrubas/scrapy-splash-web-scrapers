# ? funkcja czyszcząca "meta" w catchErrors.py
# ? przed dodaniem Error'a do bazy danych


def clearRequestMeta(meta):
    del meta['depth']
    del meta['download_timeout']
    del meta['download_slot']
    if ('ip' in meta):
        del meta['ip']
    if ('port' in meta):
        del meta['port']
    if ('splash' in meta):
        del meta['splash']
        del meta['ajax_crawlable']
        del meta['_splash_processed']
    if ('retry_times' in meta):
        del meta['retry_times']
    if ('download_latency' in meta):
        del meta['download_latency']
