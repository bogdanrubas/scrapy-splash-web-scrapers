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
    s0_category = Field()
    s1_category = Field()
    s2_category = Field()
    name = Field()
    price = Field()
    description = Field()
    images = Field()
    detals = Field()
    sizes = Field()
