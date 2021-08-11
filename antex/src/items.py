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
    name = Field()
    price_brutto = Field()
    in_stock = Field()
    sklad = Field()
    gramatura = Field()
    szerokosc = Field()
    belka = Field()
    icons = Field()
    description = Field()
