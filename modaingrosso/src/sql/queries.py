import random
from ..backup.ua import userAgents

def get_user_agent(spider):
    return([(random.choice(userAgents), '', '')])