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
    category = Field()
    sub_category = Field()
    sub_sub_category = Field()
    artykul = Field()
    name = Field()
    new_price = Field()
    old_price = Field()
    color = Field()
    sizes = Field()
    images = Field()
    description = Field()
    sizes_table = Field()
