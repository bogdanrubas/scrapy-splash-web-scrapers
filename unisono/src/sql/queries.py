import random
from ..backup.ua import userAgents

def get_user_agent(spider):
    # spider.cursor.execute(
    #     '''SELECT * FROM userAgents ORDER BY RAND() LIMIT 1''')
    # queryResult = spider.cursor.fetchall()
    # if (queryResult == []):
    #     return([(random.choice(userAgents), '', '')])
    # else:
    #     return(queryResult)

    return([(random.choice(userAgents), '', '')])