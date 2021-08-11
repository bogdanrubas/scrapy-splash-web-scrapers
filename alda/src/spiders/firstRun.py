import mysql.connector
import os
import scrapy
from scrapy import signals
from ..modules.logs.__init__ import Logs
from ..modules.formRequest.staticIP.__init__ import FormRequest
from ..sql.createTables import create_tables
from ..functions.getCategories import get_categories
from ..functions.getPages import get_pages
from ..functions.getProducts import get_products
from ..functions.getData import get_data
from ..items import Product
from ..items import Product
import base64

class FirstRunSpider(scrapy.Spider):
    project_name = 'src'
    website = 'https://al-da.eu/pl/'
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
    this_dir = (os.path.dirname(
        os.path.realpath(__file__)).replace(os.getcwd(), '')[1:]).replace('/private', 'private')
    with open(f'{this_dir}/getQuantity.lua', 'r') as file:
        get_quantity = file.read()
    products_list = []

    def parse(self, response):
        create_tables(self)
        logs = Logs()
        form_request = FormRequest()
        categories = get_categories(response, logs)

        for log in logs.add_to_db():
            yield log

        for category in categories:
            yield form_request.http(category['url'], self.get_pages, self, {
                'category': category['name'],
            })

    def get_pages(self, response):
        logs = Logs()
        form_request = FormRequest()
        pages = get_pages(response, logs)

        for log in logs.add_to_db():
            yield log

        for page in pages:
            yield form_request.http(page, self.get_products, self, {
                'category': response.meta['category'],
            })

    def get_products(self,  response):
        logs = Logs()
        form_request = FormRequest()
        products = get_products(response, logs)

        for log in logs.add_to_db():
            yield log

        for product in products:
            self.products_list.append({
                'url': product,
                'parsing': False,
                'parsed': False
            })

        for i in range(0, len(self.products_list)):
            url = self.products_list[i]['url']
            parsing = self.products_list[i]['parsing']
            parsed = self.products_list[i]['parsed']

            if parsed == False and parsing == False:
                parsing = True
                yield form_request.executeJS(url, self.get_product_data, self.get_quantity, self, {
                    'category': response.meta['category'],
                    'i': i
                })

    def get_product_data(self, response):
        product = Product()
        logs = Logs()

        data = get_data(response, logs)
        self.products_list[response.meta['i']]['parsing'] = False
        self.products_list[response.meta['i']]['parsed'] = True

        for log in logs.add_to_db():
            yield log

        product['url'] = data['url']
        product['category'] = data['category']
        product['name'] = data['name']
        product['color'] = data['color']
        product['images'] = data['images']
        product['description'] = data['description']
        product['size_table'] = data['size_table']

        yield product
