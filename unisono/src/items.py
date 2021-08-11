from scrapy import Item, Field

class Log(Item):
    time = Field()
    type = Field()
    location = Field()
    url = Field()
    description = Field()

class Product(Item):
    artykul = Field()
    category = Field()
    sub_category = Field()
    sub_sub_category = Field()
    color = Field()
    url = Field()
    name = Field()
    old_price = Field()
    new_price = Field()
    description = Field()
    color = Field()
    images = Field()
    sizes = Field()

class Error(Item):
    depth = Field()
    url = Field()
    meta = Field()