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
    spider.cursor.execute(
        '''SELECT * FROM userAgents ORDER BY RAND() LIMIT 1''')
    queryResult = spider.cursor.fetchall()
    if (queryResult == []):
        return([(random.choice(userAgents), '', '')])
    else:
        return(queryResult)