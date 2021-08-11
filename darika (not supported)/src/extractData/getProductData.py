import os
from ..modules.logs.addLog import add_error

#produkt name -
product_name_css = 'body > div > table > tbody > tr > td > table:nth-child(2) > tbody > tr > td:nth-child(2) > form > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(1) > td:nth-child(1) > span::text'
producer_name_css = 'body > div > table > tbody > tr > td > table:nth-child(2) > tbody > tr > td:nth-child(2) > form > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(3) > td > span::text'
p_css = '.main > p'
image_css = '.main table > tbody > tr:nth-child(1) > td > img::attr(src)'
price_css = 'body > div > table > tbody > tr > td > table:nth-child(2) > tbody > tr > td:nth-child(2) > form > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(1) > td:nth-child(2) > span::text'

def get_product_data(response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.url

    product = {
        'url': actual_url,
        'brand' : '',
        'product': '',
        'description': '',
        'size':'',
        'image': '',
        'price': 0
    }

    # @brand
    brand = response.css(producer_name_css).get()
    if (brand == None):
        add_error('brand', producer_name_css, logs, file_path, actual_url)
    else:
        product['brand'] = brand.split('cent:')[1].strip()
    # @name
    name = response.css(product_name_css).get()
    if (name == None):
        add_error('product', product_name_css, logs, file_path, actual_url)
    else:
        product['product'] = name

    # # @images
    image = response.css(image_css).get()
    if (image == []):
        add_error('images', image_css, logs, file_path, actual_url)
    else:
        product['image'] = image

    # # @price
    price = response.css(price_css).get()
    if price == None:
        add_error('price', price_css, logs, file_path, actual_url)
    else:
        product['price'] = float(
            price.strip().replace('zł', '').replace(',', '.'))
    #<p>
    ps = response.css(p_css)
    ps_list=[]

    for p in ps:
      pcont= p.get()
      if "Opakowanie:" in pcont:
        size = pcont.replace('<p>', '').replace('</p>', '').split('wanie:')[1]
        product['size']=size.strip()
      else:
        ps_list.append(pcont)
      product['description'] = ps_list

    return product
