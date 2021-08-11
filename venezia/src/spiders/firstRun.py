import scrapy
from scrapy import signals
import os
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TCPTimedOutError
from ..items import Product
from ..crawlers.getCategories import get_categories
from ..crawlers.getRestOfCategories import get_rest_of_categories
from ..crawlers.getPages import get_pages
from ..crawlers.getProducts import get_products
from ..crawlers.getProduct import get_product
from ..modules.logs.__init__ import Logs
from ..modules.formRequest.staticIP.__init__ import FormRequest
import mysql.connector
from ..sql.createTables import create_tables
from ..items import Log


class FirstRunSpider(scrapy.Spider):
    projectName = 'src'
    website = 'https://www.venezia.pl'
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
            projectName + '.pipelines.AddToDb': 400
        }
    }

    def parse(self, response):
        create_tables(self, 0)
        form_request = FormRequest()
        logs = Logs()
        categories = get_categories(self, response, logs)

        for log in logs.add_to_db():
            yield log

        for category in categories:
            url = self.website + category['url']

            yield form_request.waitForSelector(url, self.get_all_sub_sub_categories, '#left_menu', self, {}, {
                'category': category['name']
            })

    def get_all_sub_sub_categories(self, response):
        form_request = FormRequest()
        logs = Logs()
        sub_categories = get_rest_of_categories(self, response, logs, response.meta.get('category'))

        for log in logs.add_to_db():
            yield log

        for sub_category in sub_categories:
            if 'sub_categories' not in sub_category:
                url = self.website + sub_category['url']

                yield form_request.checkIfExists(url, self.getAllPages, '.pages_list > a', 5, self, {
                    'actual_url': url,
                    'category': response.meta.get('category'),
                    'sub_category': sub_category['name'],
                    'subsub_category': ''
                })
            else:
                for sub_sub_category in sub_category['sub_categories']:
                    url = self.website + sub_sub_category['url']
                    yield form_request.checkIfExists(url, self.get_all_pages, '.pages_list > a', 5, self, {
                        'actual_url': url,
                        'category': response.meta.get('category'),
                        'sub_category': sub_category['name'],
                        'sub_sub_category': sub_sub_category['name']
                    })

    def get_all_pages(self, response):
        logs = Logs()
        form_request = FormRequest()
        pagination_exists = response.data['isExists']
        pages = get_pages(self, response, pagination_exists, self.website, logs)

        for log in logs.add_to_db():
            yield log

        for page in pages:
            yield form_request.waitForSelector(page, self.get_all_products, '.product_box > .row', self, {}, {
                'actual_url': page,
                'category': response.meta.get('category'),
                'sub_category': response.meta.get('sub_category'),
                'sub_sub_category': response.meta.get('sub_sub_category')
            })

    def get_all_products(self, response):
        logs = Logs()
        form_request = FormRequest()
        products = get_products(self, response, self.website, logs)

        for log in logs.add_to_db():
            yield log

        for product in products:
            yield form_request.waitForSelector(product, self.get_product_data, '#content', self, {}, {
                'actual_url': product,
                'category': response.meta.get('category'),
                'sub_category': response.meta.get('sub_category'),
                'sub_sub_category': response.meta.get('sub_sub_category')
            })

    def get_product_data(self, response):
        logs = Logs()
        product = Product()
        product_data = get_product(self, response, logs)

        for log in logs.add_to_db():
            yield log

        product['url'] = product_data['url']
        product['category'] = product_data['category']
        product['sub_category'] = product_data['sub_category']
        product['sub_sub_category'] = product_data['sub_sub_category']
        product['artykul'] = product_data['artykul']
        product['name'] = product_data['name']
        product['color'] = product_data['color']
        product['old_price'] = product_data['old_price']
        product['new_price'] = product_data['new_price']
        product['description'] = product_data['description']
        product['description_table'] = product_data['description_table']
        product['sizes'] = product_data['sizes']
        product['images'] = product_data['images']
        yield product
