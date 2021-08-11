from scrapy import Item, Field

class Error(Item):
    depth = Field()
    url = Field()
    meta = Field()

class Log(Item):
    time = Field()
    type = Field()
    location = Field()
    url = Field()
    description = Field()

class Product(Item):
    url = Field()
    available = Field()
    category = Field()
    name = Field()
    new_price = Field()
    old_price = Field()
    images = Field()
    description = Field()
    sizes = Field()
    colors = Field()
