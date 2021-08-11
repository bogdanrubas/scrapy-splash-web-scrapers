import os
from ..modules.logs.addLog import add_error

product_name_css = 'h1::text'
description_css = '.full-description p::text'
images_css = '.picture-thumbs > a'
image_css = 'a::attr(src)'

def get_product_data(response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.url

    product = {
        'categories':'',
        'url': actual_url,
        'name': '',
        'description': '',
        'images': []
    }

    # @name
    name = response.css(product_name_css).get()

    if (name == None):
        add_error('name', product_name_css, logs, file_path, actual_url)
    else:
        product['name'] = name[0:name.find('–') - 1].strip()

    # @description
    description = response.css(description_css).get()

    if (description == None):
        add_error('description', description_css, logs, file_path, actual_url)
    else:
        product['description'] = description

    # @images
    images_list = []
    images = response.css(images_css)

    if (images == []):
        add_error('images', images_css, logs, file_path, actual_url)
    else:
        for image in images:
            image_href = image.css("::attr(href)")

            if image_href == None:
                add_error('image_href', image_css, logs, file_path, actual_url)
            else:
              if image_href in images_list:
                pass
              else:
                if image_href not in images_list:
                  images_list.append(image_href.get())

    product['images'] = images_list
    return product
