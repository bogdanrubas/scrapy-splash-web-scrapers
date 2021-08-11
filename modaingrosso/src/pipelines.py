import mysql.connector
import random
from .items import Log, Error, Product
from .sql.mutations import add_log_to_db, add_error_to_db, add_product_to_db

class AddToDb(object):
    def process_item(self, item, spider):
        if isinstance(item, Log):
            add_log_to_db(spider, item)

        if isinstance(item, Error):
            add_error_to_db(spider, item)

        if isinstance(item, Product):
            add_product_to_db(item)

        return item
