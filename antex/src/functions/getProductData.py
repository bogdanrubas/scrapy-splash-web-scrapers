import os
from ..modules.logs.addLog import add_error

# product: {
# - url: string
# - category: string
# - sub_category: string
# - sub_sub_category: string
# - name: string
# - price_brutto: float
# - in_stock: boolean
# - sklad: string
# - gramatura: string
# - belka: string
# - icons: string
# - description: string
# }


def get_product_data(self, response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]

    actual_url = response.meta.get('actual_url')
    product = {}
    product['url'] = response.meta.get('actual_url')
    product['category'] = response.meta.get('category')
    product['sub_category'] = response.meta.get('sub_category')
    product['name'] = ''
    product['price_brutto'] = ''
    product['in_stock'] = True
    product['sklad'] = ''
    product['gramatura'] = ''
    product['szerokosc'] = ''
    product['belka'] = ''
    product['icons'] = ''
    product['description'] = ''

    # @name
    name_css = 'h1.h1::text'
    name = response.css(name_css).get()
    if (name == None):
        add_error('name', name_css, logs, file_path, actual_url)
    else:
        product['name'] = name

    # @price_brutto
    price_brutto_css = '.current-price span::attr(content)'
    price_brutto = response.css(price_brutto_css).get()
    if (price_brutto == None):
        add_error('price_brutto', price_brutto_css, logs, file_path, actual_url)
    else:
        product['price_brutto'] = float(price_brutto.replace(
            ' zł', '').replace(',', '.').strip())

    # @in_stock
    in_stock_css = '.js-mailalert'
    in_stock = response.css(in_stock_css).get()
    if (in_stock == None):
        product['in_stock'] = False

    # @icons
    icons = ''
    tds = response.css('.product-description table tr td')
    for td in tds:
        icon = td.css('img')
        icon_src = icon.css('::attr(src)').get()
        icon_text = td.css('span::text').get()
        if (icon_src != None):
          if (icon_src.find('sklad') != -1):
              product['sklad'] = icon_text.strip().replace('\xa0', '')
          if (icon_src.find('gramatura') != -1):
              product['gramatura'] = icon_text.strip().replace('\xa0', '')
          if (icon_src.find('szerokosc') != -1):
              product['szerokosc'] = icon_text.strip().replace('\xa0', '')
          if (icon_src.find('belka') != -1):
              product['belka'] = icon_text.strip().replace('\xa0', '')
          icons += '<br/>' + icon_text.strip().replace('\xa0', '')
    product['icons'] = icons.replace('\xa0', '')

    # @description
    description = ''
    p_tags = response.css('.product-description > p')
    for p in p_tags:
        p_text = p.css('::text').get()
        if (p_text != None):
            description += str(p_text)
    product['description'] = description.replace('\xa0', '')

    # @images
    images_list = []
    images_css = '.product-images li'
    image_url_css = 'img::attr(src)'
    images = response.css(images_css)
    if (images == None):
        add_error('images', images_css, logs, file_path, actual_url)
    else:
        for image in images:
            # @image
            image_url = image.css(image_url_css).get()
            if (image == None):
                add_error('image', image_url_css, logs, file_path, actual_url)
            else:
                images_list.append(image_url)
        product['images'] = images_list
    return product
