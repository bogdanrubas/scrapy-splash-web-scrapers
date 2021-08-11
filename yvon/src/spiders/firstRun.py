import mysql.connector
import os
import platform
import scrapy
from scrapy import signals
from ..modules.logs.__init__ import Logs
from ..modules.formRequest.staticIP.__init__ import FormRequest
from ..sql.createTables import create_tables
from ..extractData.getAllCategories import get_all_categories
from ..extractData.getProducts import get_products
from ..extractData.getProductData import get_product_data
from ..items import Product
import base64
from datetime import datetime


class FirstRunSpider(scrapy.Spider):
    project_name = 'src'
    acceptable_categories_list = [
        'kolekcje',
    ]
    website = 'https://yvon.pl'
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
    name = 'firstRun'
    start_urls = [
        website,
    ]
    this_dir = (os.path.dirname(
        os.path.realpath(__file__)).replace(os.getcwd(), '')[1:]).replace('/private', 'private')
    with open(f'{this_dir}/splash/signIn.lua') as file:
        sign_in = file.read()
    with open(f'{this_dir}/splash/scrollToBottom.lua') as file:
        scroll_to_bottom = file.read()

    def parse(self, response):
        create_tables(self, 0)
        form_request = FormRequest()
        logs = Logs()
        categories = get_all_categories(self.acceptable_categories_list, response, logs)

        for log in logs.add_to_db():
            yield log

        for category in categories:
            yield form_request.executeJS(self.website + category['url'], self.get_products, self.scroll_to_bottom, self, {
                'categories': [category['name']]
            })


    #     yield form_request.executeJS(response.url, self.after_sign_in, self.sign_in, self, {}, {})

    # def after_sign_in(self, response):
    #     logs = Logs()
    #     form_request = FormRequest()
    #     cookies = response.data['cookies']
    #     categories = get_all_categories(self.acceptable_categories_list, response, logs)

    #     for log in logs.add_to_db():
    #         yield log

    #     for category in categories:
    #         yield form_request.executeJS(category['url'], self.get_products, self.scroll_to_bottom, self, cookies, {
    #             'categories': [category['name']]
    #         })

    def get_products(self, response):
        logs = Logs()
        form_request = FormRequest()
        cookies = response.data['cookies']
        products = get_products(response, logs)

        for url in products:
            yield form_request.waitForSelector(self.website + url, self.get_data, '.page-body', self, cookies, {
                'categories': response.meta['categories']
            })

    def get_data(self, response):
        product = Product()
        logs = Logs()
        data = get_product_data(response, logs)

        product['categories'] = str(response.meta['categories'])
        product['url'] = data['url']
        product['name'] = data['name']
        product['description'] = data['description']
        product['images'] = str(data['images'])

        yield product


