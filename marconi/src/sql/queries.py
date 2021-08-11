import random
from ..backup.ua import userAgents


def get_user_agent(spider):
    return([(random.choice(userAgents), '', '')])


def get_proxy(spider):
    sql = '''SELECT * FROM proxies ORDER BY RAND() LIMIT 1'''
    spider.cursor.execute(sql)
    queryResult = spider.cursor.fetchall()
    return queryResult