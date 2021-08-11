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


class FirstRunSpider(scrapy.Spider):
    project_name = 'src'
    website = 'https://www.topsecret.pl/'
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

    def parse(self, response):
        create_tables(self, 0)
        logs = Logs()
        form_request = FormRequest()
        categories = get_categories(response, logs)

        for log in logs.add_to_db():
            yield log

        for category in categories:
            for sub_category in category['subCategories']:
                for sub_sub_category in sub_category['subCategories']:
                    url = sub_sub_category['url']
                    yield form_request.waitForSelector(url, self.get_pages, "#product-list", self, {}, {
                        'actual_url': url,
                        'category': category['name'],
                        'sub_category': sub_category['name'],
                        'sub_sub_category': sub_sub_category['name']
                    })

    def get_pages(self, response):
        logs = Logs()
        form_request = FormRequest()
        pages = get_pages(response, logs)

        for log in logs.add_to_db():
            yield log

        for url in pages:
            yield form_request.waitForSelector(url, self.get_products, ".products-container .product", self, {}, {
                'actual_url': url,
                'category': response.meta.get('category'),
                'sub_category': response.meta.get('sub_category'),
                'sub_sub_category': response.meta.get('sub_sub_category')
            })

    def get_products(self, response):
        logs = Logs()
        form_request = FormRequest()
        products = get_products(response, logs)

        for url in products:
            yield form_request.waitForSelector(url, self.get_data, ".product-page", self, {}, {
                'actual_url': url,
                'category': response.meta.get('category'),
                'sub_category': response.meta.get('sub_category'),
                'sub_sub_category': response.meta.get('sub_sub_category')
            })

    def get_data(self, response):
        product = Product()
        logs = Logs()
        data = get_data(response, logs)
        print(data)

        for log in logs.add_to_db():
            yield log

        product['url'] = data['url']
        product['category'] = data['category']
        product['sub_category'] = data['sub_category']
        product['sub_sub_category'] = data['sub_sub_category']
        product['artykul'] = data['artykul']
        product['name'] = data['name']
        product['new_price'] = data['new_price']
        product['old_price'] = data['old_price']
        product['color'] = data['color']
        product['sizes'] = str(data['sizes'])
        product['images'] = str(data['images'])
        product['description'] = data['description']
        product['sizes_table'] = data['sizes_table']

        yield product
