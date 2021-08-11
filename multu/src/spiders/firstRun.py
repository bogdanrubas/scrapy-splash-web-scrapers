
import mysql.connector
import os
import platform
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
    acceptable_categories_list = [
        'KOBIETY', 'MĘŻCZYŹNI', 'DZIECI',
    ]
    acceptable_sub_categories_list = [
        'OBUWIE', 'ODZIEŻ', 'AKCESORIA',
    ]
    website = 'https://multu.pl/login'
    website_home = 'https://multu.pl'
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

    def parse(self, response):
        logs = Logs()
        form_request = FormRequest()
        create_tables(self)
        categories = get_all_categories(
            self.acceptable_categories_list, self.acceptable_sub_categories_list, response, logs)

        for log in logs.add_to_db():
            yield log

        for category in categories:
            yield form_request.checkIfExists(self.website_home + category['url'], self.get_pages, '.paginate-content', 5, self, {
                'categories': category['name']
            })


    def get_pages(self, response):
        form_request = FormRequest()
        pagination_exists = response.data['isExists']
        logs = Logs()
        pages = get_pages(response, logs, pagination_exists)

        for log in logs.add_to_db():
            yield log

        for page_url in pages:
          yield form_request.http(page_url, self.get_products, self, {
              'categories': response.meta['categories']
          })

    def get_products(self, response):
      logs = Logs()
      form_request = FormRequest()
      products_list = get_products(response, logs)

      for product_url in products_list:
        yield form_request.http(self.website_home + product_url, self.get_data, self, {
              'categories': response.meta['categories']
          })

    def get_data(self, response):
        product = Product()
        logs = Logs()
        data = get_product_data(response, logs)

        product['categories'] = response.meta['categories']
        product['url'] = data['url']
        product['name'] = data['name']
        product['description'] = data['description']
        product['sizes'] = data['sizes']
        product['images'] = data['images']
        product['new_price'] = data['new_price']
        product['old_price'] = data['old_price']
        product['producer_code'] = data['producer_code']

        yield product


