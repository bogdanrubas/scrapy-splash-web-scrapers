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
    name = Field()
    color = Field()
    images = Field()
    description = Field()
    size_table = Field()
