import mysql.connector
import os
import scrapy
from scrapy import signals
from ..modules.logs.__init__ import Logs
from ..modules.formRequest.staticIP.__init__ import FormRequest
from ..sql.createTables import create_tables
from ..functions.getCategories import get_categories
from ..functions.getProducts import get_products
from ..functions.getData import get_data
from ..items import Product

actual_dir = os.path.dirname(
    os.path.realpath(__file__)).replace(os.getcwd(), '')[1:]
with open(actual_dir + '/lua/clickShowAllProducts.lua', 'r') as file:
    click_show_all_products = file.read()


class FirstRunSpider(scrapy.Spider):
    project_name = 'src'
    website = 'https://sklep.marconi.com.pl'
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
        print('closed')

    def parse(self, response):
        create_tables(self, 0)
        logs = Logs()
        form_request = FormRequest()
        # url = 'https://sklep.marconi.com.pl/marconi-koszule/850-koszula-dla-chlopca-marconi-dlugi-rekaw-slim-line-t1221.html?search_query=t1221&results=5'
        # yield form_request.http(url,  self.get_product_data, self, {})
        categories = get_categories(response, logs)

        for log in logs.add_to_db():
            yield log

        for s0_category in categories:
            print('############################################')
            print(s0_category['name'])
            if 'subCategories' not in s0_category:
                yield form_request.waitForSelector(s0_category['url'], self.get_products, '.product_list .product_img_link', self, {}, {
                    's0_category': s0_category['name'],
                    's1_category': '',
                    's2_category': '',
                })
            else:
                for s1_category in s0_category['subCategories']:
                    print('###################')
                    print(s1_category['name'])
                    if 'subCategories' not in s1_category:
                        yield form_request.waitForSelector(s1_category['url'], self.get_products, '.product_list .product_img_link', self, {}, {
                            's0_category': s0_category['name'],
                            's1_category': s1_category['name'],
                            's2_category': '',
                        })
                    else:
                        for s2_category in s1_category['subCategories']:
                            print(s2_category['name'])
                            yield form_request.waitForSelector(s2_category['url'], self.get_products, '.product_list .product_img_link', self, {}, {
                                's0_category': s0_category['name'],
                                's1_category': s1_category['name'],
                                's2_category': s2_category['name'],
                            })

    def get_products(self,  response):
        logs = Logs()
        form_request = FormRequest()

        if (response.css('.showall').get() != None):
            yield form_request.executeJS(response.url, self.get_products, click_show_all_products, self, {
                's0_category': response.meta.get('s0_category'),
                's1_category': response.meta.get('s1_category'),
                's2_category': response.meta.get('s2_category'),
            })
        else:
            products = get_products(response, logs)

            for log in logs.add_to_db():
                yield log

            for product in products:
                yield form_request.http(product, self.get_product_data, self, {
                    's0_category': response.meta.get('s0_category'),
                    's1_category': response.meta.get('s1_category'),
                    's2_category': response.meta.get('s2_category'),
                })

    def get_product_data(self, response):
        product = Product()
        logs = Logs()
        data = get_data(response, logs)

        for log in logs.add_to_db():
            yield log

        product['url'] = data['url']
        product['s0_category'] = data['s0_category']
        product['s1_category'] = data['s1_category']
        product['s2_category'] = data['s2_category']
        product['name'] = data['name']
        product['price'] = data['price']
        product['description'] = data['description']
        product['images'] = data['images']
        product['detals'] = data['detals']
        product['sizes'] = data['sizes']

        yield product
