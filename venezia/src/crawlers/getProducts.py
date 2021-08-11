import os
from ..modules.logs.addLog import add_error


def get_products(self, response, website, logs):
    filePath = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.meta.get('actual_url')
    # @products
    products_list = []
    products_css = '.product_box > .row a'
    product_css = '::attr(href)'
    products = response.css(products_css)

    if (products == []):
        add_error('products', product_css, logs, filePath, actual_url)
    else:
        for product in products:
            # @product
            url = product.css(product_css).get()
            if (product == None):
                add_error('product', product_css, logs, filePath, actual_url)
            else:
                products_list.append(website + url)
    return products_list
