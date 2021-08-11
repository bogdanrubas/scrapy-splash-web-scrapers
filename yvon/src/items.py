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
    categories = Field()
    url = Field()
    name = Field()
    description = Field()
    images = Field()
