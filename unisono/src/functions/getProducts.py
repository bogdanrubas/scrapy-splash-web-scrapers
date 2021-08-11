import os
from ..modules.logs.addLog import add_error

# products_list: [{
# - url: string (ex. https://example.com/product1)
# - category: string
# - sub_category: string
# - sub_sub_category: string
# }]


def get_products(self, response, logs, website):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.request.url

    # @products
    products_list = []
    products_css = '.product-list > div > .list-product-item'
    product_css = 'a::attr(href)'
    products = response.css(products_css)
    if (products == []):
        add_error('products', products_css, logs, file_path, actual_url)
    else:
        for product in products:
            # @product
            url = product.css(product_css).get()
            if (url == None):
                add_error('product', product_css, logs, file_path, actual_url)
            else:
                products_list.append({
                    'url': website + url,
                    'category': response.meta.get('category'),
                    'sub_category': response.meta.get('sub_category'),
                    'sub_sub_category': response.meta.get('sub_sub_category')
                })

    return(products_list)
