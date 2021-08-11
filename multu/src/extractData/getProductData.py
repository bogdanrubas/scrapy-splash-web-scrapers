import os
from ..modules.logs.addLog import add_error


product_name_css = '.product-description .name::text'
description_css = '#details > div > div > div > div ul > li'
sizes_css = '.select-size-container > .size > label.size-label'
size_name_css = '.size-value::text'
size_available_css = '.not-available::text'
size_available=''
images_css = '.thumb-slider-box > .thumb-slider-container > .swiper-container > .swiper-wrapper > .swiper-slide'
image_css = 'img::attr(data-src)'
price_css = '.price'
product_code_css = "div.product-description > p::text"

def get_product_data(response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.url

    product = {
        'categories': response.meta['categories'],
        'url': actual_url,
        'name': '',
        'description': '',
        'sizes': [],
        'images': [],
        'new_price': 0,
        'old_price': 0,
        'producer_code': ''
    }

    # @name
    name = response.css(product_name_css).get()
    if (name == None):
        add_error('name', product_name_css, logs, file_path, actual_url)
    else:
        product['name'] = name[0:name.find('–') - 1].strip()

    # @producerCode
    producer_code = response.css(product_code_css).get()
    if (name == None):
        add_error('name', product_name_css, logs, file_path, actual_url)
    else:
        product['producer_code'] = producer_code.split("produktu:")[1].strip()

    description_out=""
    descriptions = response.css(description_css)
    if (descriptions ==[]):
        add_error('description', description_css, logs, file_path, actual_url)
    else:
      for item_description in descriptions:
        item_desc = item_description.css('::text').get()
        if 'color:' in item_desc:
          color = item_desc.split(":")[1].strip()
          product['color']=color

        if 'Wymiary produktu' not in item_desc:
          description_out += '<p>'+item_desc+"</p>"

      product['description'] = description_out

    # @sizes
    sizes_list = []
    sizes = response.css(sizes_css)

    if (sizes == []):
        add_error('sizes', sizes_css, logs, file_path, actual_url)
    else:
        for size in sizes:
          size_name = size.css(size_name_css).get()

          if 'POŚPIESZ' in size_name:
            size_name = size_name.split('POŚPIESZ')[0]
          size_available = size.css(size_available_css).get()
          if size_name == None:
              add_error('size_name', size_name_css,
                        logs, file_path, actual_url)
          else:
            if size_available == None:
              sizes_list.append(size_name)
    product['sizes'] = sizes_list

    # @images
    images_list = []
    images = response.css(images_css)
    if (images == []):
        add_error('images', images_css, logs, file_path, actual_url)
    else:
        for image in images:
            image_href = image.css(image_css).get()
            if image_href == None:
                add_error('image_href', image_href, logs, file_path, actual_url)
            else:
              if image_href in images_list:
                pass
              else:
                img1 = image_href
                images_list.append(img1)

    product['images'] = images_list

    # @price
    price = response.css(price_css)
    old=0
    try:
      old = price.css('.old::text').get().replace('zł','')
    except:
      old = price.css('.original-price::text').get().replace('zł', '')
    try:
      new = price.css('.new::text').get().replace('zł', '')
    except:
      new=old

    if old == None:
        add_error('price', price_css, logs, file_path, actual_url)
    else:
        product['old_price'] = float(old.strip().replace(',', '.'))
        product['new_price'] = float(new.strip().replace(',', '.'))
    return product
