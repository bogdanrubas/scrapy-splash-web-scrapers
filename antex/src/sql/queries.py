import random
from ..backup.ua import userAgents


def get_errors(spider, runCount):
    index = str(int(runCount) - 1)
    spider.cursor.execute(f'''SELECT * FROM errors{index}''')
    queryResultErrors = spider.cursor.fetchall()
    return queryResultErrors


def get_proxy(spider):
    spider.cursor.execute(f'''SELECT * FROM proxies''')
    queryResultErrors = spider.cursor.fetchall()
    return queryResultErrors


def get_user_agent(spider):
    return([(random.choice(userAgents), '', '')])