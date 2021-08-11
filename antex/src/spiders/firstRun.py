import mysql.connector
import os
import scrapy
from scrapy import signals
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TCPTimedOutError
from ..modules.logs.__init__ import Logs
from ..modules.formRequest.staticIP.__init__ import FormRequest
from ..sql.createTables import create_tables
from ..functions.getCategories import get_categories
from ..functions.getProducts import get_products
from ..functions.getProductData import get_product_data
from ..items import Product

actual_dir = os.path.dirname(
    os.path.realpath(__file__)).replace(os.getcwd(), '')[1:]
with open(actual_dir + '/lua/clickShowAllProducts.lua', 'r') as file:
    click_show_all_products = file.read()


class FirstRunSpider(scrapy.Spider):
    project_name = 'src'
    website = 'https://bawelna-tkaniny.pl/pl/'
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='ae321321',
        database='bots',
        buffered=True
    )
    cursor = connection.cursor()
    name = 'firstRun'
    start_urls = [
        website
    ]
    custom_settings = {
        'ITEM_PIPELINES': {
            project_name + '.pipelines.AddToDb': 400
        }
    }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(FirstRunSpider, cls).from_crawler(
            crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed,
                                signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        pass

    def parse(self, response):
        create_tables(self, 0)
        logs = Logs()
        form_request = FormRequest()
        categories = get_categories(self, response, logs)

        for log in logs.add_to_db():
            yield log

        for category in categories:
          if ('sub_categories' not in category):
            pass
          else:
            for sub_category in category['sub_categories']:
              yield form_request.waitForSelector(
                  sub_category['url'],
                  self.get_all_products,
                  '#js-product-list article',
                  self,
                  {},
                  {
                      'category': category['name'],
                      'sub_category': sub_category['name']
                  }
              )

    def get_all_products(self, response):
        form_request = FormRequest()
        logs = Logs()
        products = get_products(self, response, logs)

        for log in logs.add_to_db():
            yield log

        for product in products:
            yield form_request.http(
                product['url'],
                self.get_product_data,
                self,
                {
                    'actual_url': product['url'],
                    'category': response.meta.get('category'),
                    'sub_category': response.meta.get('sub_category')
                }
            )

    def get_product_data(self, response):
        print("get_product_data")
        logs = Logs()
        product = Product()
        product_data = get_product_data(self, response, logs)

        for log in logs.add_to_db():
            yield log

        product['url'] = product_data['url']
        product['category'] = product_data['category']
        product['sub_category'] = product_data['sub_category']
        product['name'] = product_data['name']
        product['price_brutto'] = product_data['price_brutto']
        product['in_stock'] = product_data['in_stock']
        product['sklad'] = product_data['sklad']
        product['gramatura'] = product_data['gramatura']
        product['szerokosc'] = product_data['szerokosc']
        product['belka'] = product_data['belka']
        product['icons'] = product_data['icons']
        product['description'] = product_data['description']

        yield product
        # print(product)
