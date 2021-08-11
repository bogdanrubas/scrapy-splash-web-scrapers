import os
from ..modules.logs.addLog import add_error


def get_products(response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.url
    # @products
    products_list = []
    products_css = 'ul.products > li > div'
    product_css = 'a::attr(href)'
    products = response.css(products_css)
    if (products == []):
        add_error('products', product_css, logs, file_path, actual_url)
    else:
        for product in products:
            # @product
            url = product.css(product_css).get()
            if (product == None):
                add_error('product', product_css, logs, file_path, actual_url)
            else:
                products_list.append(url)
    return products_list
