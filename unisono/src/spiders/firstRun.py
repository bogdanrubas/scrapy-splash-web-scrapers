import scrapy
from scrapy import signals
import os
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TCPTimedOutError
from ..items import Product
from ..functions.getCategories import get_categories
from ..functions.getPages import get_pages
from ..functions.getProducts import get_products
from ..functions.getProduct import get_product
from ..functions.getColors import get_colors
from ..modules.logs.__init__ import Logs
from ..modules.formRequest.staticIP.__init__ import FormRequest
from ..sql.createTables import create_tables
import mysql.connector

class FirstRunSpider(scrapy.Spider):
    projectName = 'src'
    website = 'https://www.unisono.eu'
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
        create_tables(self)
        url_suffix = "-default/180"
        css_selector = ".pagination > li"
        form_request = FormRequest()
        logs = Logs()
        categories = get_categories(self, response, logs)
        for add in logs.add_to_db():
            yield add

        for category in categories:
            for sub_category in category['subCategories']:
                for sub_sub_category in sub_category['subCategories']:
                    page_url = self.website + \
                        sub_sub_category['url'] + url_suffix

                    yield form_request.waitForSelector(
                        page_url,
                        self.get_all_pages,
                        css_selector,
                        self,
                        {},
                        {
                            'actual_url': page_url,
                            'category': category['name'],
                            'sub_category': sub_category['name'],
                            'sub_sub_category': sub_sub_category['name']
                        }
                    )

    def get_all_pages(self, response):
        css_selector = '#content-main > .product-list > div > .list-product-item'
        logs = Logs()
        pages = get_pages(self, response, logs, self.website)

        for add in logs.add_to_db():
            yield add

        for page_url in pages:
            form_request = FormRequest()
            yield form_request.waitForSelector(
                page_url,
                self.get_all_products,
                css_selector,
                self,
                {},
                {
                    'actual_url': page_url,
                    'category': response.meta.get('category'),
                    'sub_category': response.meta.get('sub_category'),
                    'sub_sub_category': response.meta.get('sub_sub_category')
                }
            )

    def get_all_products(self, response):
        logs = Logs()
        products = get_products(self, response, logs, self.website)

        for add in logs.add_to_db():
            yield add

        for product in products:
            form_request = FormRequest()
            yield form_request.http(
                product['url'],
                self.get_all_colors,
                self,
                {
                    'category': response.meta.get('category'),
                    'sub_category': response.meta.get('sub_category'),
                    'sub_sub_category': response.meta.get('sub_sub_category')
                }
            )

    def get_all_colors(self, response):
        logs = Logs()
        colors_links = get_colors(self, response, logs, self.website)

        for add in logs.add_to_db():
            yield add

        for link in colors_links:
            form_request = FormRequest()
            yield form_request.http(
                link,
                self.get_product_data,
                self,
                {
                    'actual_url': link,
                    'category': response.meta.get('category'),
                    'sub_category': response.meta.get('sub_category'),
                    'sub_sub_category': response.meta.get('sub_sub_category')
                }
            )

    def get_product_data(self, response):
        logs = Logs()
        product = Product()
        product_data = get_product(self, response, logs)

        for add in logs.add_to_db():
            yield add

        product['artykul'] = product_data['artykul']
        product['url'] = product_data['url']
        product['category'] = product_data['category']
        product['sub_category'] = product_data['sub_category']
        product['sub_sub_category'] = product_data['sub_sub_category']
        product['color'] = product_data['color']
        product['name'] = product_data['name']
        product['description'] = product_data['description']
        product['images'] = product_data['images']
        product['sizes'] = product_data['sizes']
        product['old_price'] = product_data['old_price']
        product['new_price'] = product_data['new_price']

        yield product
