from datetime import datetime
from ...items import Log


class Logs:
    def __init__(self):
        self.items = []

    def add_to_db(self):
        log = Log()
        logList = []
        for item in self.items:
            log['time'] = item['time']
            log['type'] = item['type']
            log['location'] = item['location']
            log['url'] = item['url']
            log['description'] = item['description']
            logList.append(log)
        return logList

    def add(self, type, location, description, url):
        log = {}
        log = {
            'time': datetime.now().strftime("%H:%M:%S"),
            'type': type,
            'location': location,
            'url': url,
            'description': description
        }
        self.items.append(log)
