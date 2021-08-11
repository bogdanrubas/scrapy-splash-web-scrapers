import mysql.connector
import os
import scrapy
from scrapy import signals
from ..modules.logs.__init__ import Logs
from ..modules.formRequest.staticIP.__init__ import FormRequest
from ..sql.createTables import create_tables
from ..extractData.getAllCategories import get_all_categories
from ..extractData.getPages import get_pages
from ..extractData.getProducts import get_products
from ..extractData.getProductData import get_product_data
from ..items import Product
import base64
from datetime import datetime

class FirstRunSpider(scrapy.Spider):
    project_name = 'src'
    not_acceptable_categories_list = [
        'bluzki',
        'dresy',
        'spódnice',
        'sukienki',
        'spodnie',
        'tuniki',
    ]
    website = 'https://alekssandra.pl/my-account/'
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='ae321321',
        database='bots',
        buffered=True
    )
    cursor = connection.cursor()
    custom_settings = {
        'ITEM_PIPELINES': {
            project_name + '.pipelines.AddToDb': 400
        }
    }
    cursor = connection.cursor()
    name = 'firstRun'
    start_urls = [
        website,
    ]
    this_dir = (os.path.dirname(
        os.path.realpath(__file__)).replace(os.getcwd(), '')[1:]).replace('/private', 'private')
    with open(f'{this_dir}/lua/closeModalAndLogin.lua', 'r') as file:
        close_modal_and_login = file.read()

    def parse(self, response):
        create_tables(self)
        form_request = FormRequest()
        yield form_request.executeJS(response.url, self.after_login, self.close_modal_and_login, self, {})

    def after_login(self, response):
        cookies = response.data['cookies']
        url = 'https://alekssandra.pl/kategoria-produktu/nowosci/'
        form_request = FormRequest()

        yield form_request.waitForSelector(url, self.get_all_categories, 'div', self, cookies, {})

    def get_all_categories(self, response):
        cookies = response.data['cookies']
        logs = Logs()
        form_request = FormRequest()
        categories = get_all_categories(
            self.not_acceptable_categories_list, response, logs)

        for log in logs.add_to_db():
            yield log

        for category in categories:
            yield form_request.checkIfExists(category['url'], self.get_pages, '.woocommerce-pagination', 2, self, cookies, {
                'categories': [category['name']]
            })

    def get_pages(self, response):
        cookies = response.data['cookies']
        logs = Logs()
        form_request = FormRequest()
        pagination_exists = response.data['isExists']

        if pagination_exists:
            pages = get_pages(response, logs)

            for log in logs.add_to_db():
                yield log
            for url in pages:
                yield form_request.waitForSelector(url, self.get_products, 'div', self, cookies, {
                    'categories': response.meta['categories'],
                })
        else:
            yield form_request.waitForSelector(response.url, self.get_products, 'div', self, cookies, {
                'categories': response.meta['categories'],
            })

    def get_products(self,  response):
        cookies = response.data['cookies']
        logs = Logs()
        form_request = FormRequest()
        categories = response.meta['categories']
        products = get_products(response, logs)

        for log in logs.add_to_db():
            yield log

        for product_url in products:
            yield form_request.http(product_url, self.get_product_data, self, cookies, {
                'categories': response.meta['categories'],
            })

    def get_product_data(self, response):
        logs = Logs()
        product = Product()
        data = get_product_data(response, logs)

        for log in logs.add_to_db():
            yield log

        product['categories'] = response.meta['categories']
        product['url'] = data['url']
        product['name'] = data['name']
        product['description'] = data['description']
        product['colors'] = data['colors']
        product['sizes'] = data['sizes']
        product['images'] = data['images']
        product['price'] = data['price']

        yield product
