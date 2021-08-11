import os
from ..modules.logs.addLog import add_error

# products_list: [{
# - url: string (ex. https://example.com/product1)
# }]


def get_products(self, response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actualUrl = response.request.url

    # @products
    products_list = []
    products_css = '#js-product-list .product-miniature'
    product_css = 'a::attr(href)'
    products = response.css(products_css)
    if (products == []):
        add_error('products', products_css, logs, file_path, actualUrl)
    else:
        for product in products:
            # @product
            url = product.css(product_css).get()
            if (url == None):
                add_error('product', product_css, logs, file_path, actualUrl)
            else:
                products_list.append({
                    'url': url
                })

    return(products_list)
