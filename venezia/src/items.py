# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

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
    category = Field()
    sub_category = Field()
    sub_sub_category = Field()
    url = Field()
    artykul = Field()
    name = Field()
    color = Field()
    new_price = Field()
    old_price = Field()
    sizes = Field()
    images = Field()
    description = Field()
    description_table = Field()
