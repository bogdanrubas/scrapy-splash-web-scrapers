import os
from ..modules.logs.addLog import add_error


product_name_css = '.product_title::text'
description_css = '.woocommerce-product-details__short-description > p:first-of-type::text'
colors_css = '#pa_kolor > option'
color_css = '::text'
sizes_css = '.swatchinput'
size_name_css = 'label::text'
images_css = '.product_images > .product-image'
image_css = 'a::attr(href)'
price_css = 'p.price .woocommerce-Price-amount > bdi::text'

def get_product_data(response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.url

    product = {
        'url': actual_url,
        'name': '',
        'description': '',
        'colors': [],
        'sizes': [],
        'images': [],
        'price': 0
    }

    # @name
    name = response.css(product_name_css).get()
    if (name == None):
        add_error('name', product_name_css, logs, file_path, actual_url)
    else:
        product['name'] = name[0:name.find('(')]

    # @description
    description = response.css(description_css).get()
    if (description == None):
        add_error('description', description_css, logs, file_path, actual_url)
    else:
        product['description'] = description

    # @colors
    colors_list = []
    colors = response.css(colors_css)
    if (name == []):
        add_error('colors', colors_css, logs, file_path, actual_url)
    else:
        for i in range(1, len(colors)):
            colors_list.append(colors[i].css(color_css).get())
    product['colors'] = colors_list

    # @sizes
    sizes_list = []
    sizes = response.css(sizes_css)
    if (sizes == []):
        add_error('sizes', sizes_css, logs, file_path, actual_url)
    else:
        for size in sizes:
            size_name = size.css(size_name_css).get()
            if size_name == None:
                add_error('size_name', size_name_css, logs, file_path, actual_url)
            else:
                sizes_list.append(size_name)
    product['sizes'] = sizes_list

    # @images
    images_list = []
    images = response.css(images_css)
    if (images == []):
        add_error('images', images_css, logs, file_path, actual_url)
    else:
        for image in images:
            imageHref = image.css(image_css).get()
            if imageHref == None:
                add_error('imageHref', imageHrefCss, logs, file_path, actual_url)
            else:
                images_list.append(imageHref)
    product['images'] = images_list

    # @price
    price = response.css(price_css).get()
    if price == None:
        add_error('price', price_css, logs, file_path, actual_url)
    else:
        product['price'] = float(price.strip().replace(',', '.'))
    return product
