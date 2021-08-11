import os
from ..modules.logs.addLog import add_error

product_name_css = '.product_title::text'
description_css = 'div.woocommerce-product-details__short-description::text'
sizes_css = '#pa_rozmiar > option'
size_name_css = '::text'
images_css = '.product_thumbnails.flex-control-nav > li > img'
image_css = 'a::attr(href)'
price_css = '.price .woocommerce-Price-amount.amount > bdi::text'

def color(name):
  if name.find('–') > 0:
    start_ = name.find('–')+1
    lenght_ = len(name)

    return name[start_:lenght_].strip()
  else:
    return '-------'

def get_product_data(response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.url

    product = {
        'categories':'',
        'url': actual_url,
        'name': '',
        'color':'',
        'description': '',
        'sizes': [],
        'images': []
    }

    # @name
    name = response.css(product_name_css).get()
    if (name == None):
        add_error('name', product_name_css, logs, file_path, actual_url)
    else:
        product['name'] = name[0:name.find('–') - 1].strip()
        product['color'] = color(name)

    # @description
    description = response.css(description_css).get()
    if (description == None):
        add_error('description', description_css, logs, file_path, actual_url)
    else:
        product['description'] = description

    # @sizes
    sizes_list = []
    sizes = response.css(sizes_css)
    if (sizes == []):
        add_error('sizes', sizes_css, logs, file_path, actual_url)
    else:
        for i in range(0, len(sizes)):
            if i > 0:
                size_name = sizes[i].css(size_name_css).get()
                if size_name == None:
                    add_error('size_name', size_name_css,
                             logs, file_path, actual_url)
                else:
                    sizes_list.append(size_name)
    product['sizes'] = sizes_list

    # @images
    images_list = []
    first_image_css = ".product-images-wrapper img::attr(src)"
    first_image = response.css(first_image_css).get().split("uploads/")[-1]
    images_list.append(first_image)
    images = response.css(images_css)
    if (images == []):
        add_error('images', images_css, logs, file_path, actual_url)
    else:
        for image in images:
            image_href = image.css("::attr(src)").get().split("uploads/")[-1].split("-")[0]+".jpg"
            if image_href == None:
                add_error('image_href', image_css, logs, file_path, actual_url)
            else:
              if image_href in images_list:
                pass
              else:
                if image_href not in images_list:
                  images_list.append(image_href)

    product['images'] = images_list

    return product
