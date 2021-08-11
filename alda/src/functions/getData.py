import os
from ..modules.logs.addLog import add_error

def get_data(response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.url

    product = {
        'url': '',
        'category': '',
        'name': '',
        'color': '',
        'images': [],
        'description': '',
        'size_table': '',
    }
    product['url'] = actual_url
    product['category'] = response.meta.get('category')

    # @name
    name_css = 'h1.pd-name::text'
    name = response.css(name_css).get()
    if (name == None):
        add_error('name', name_css, logs, file_path, actual_url)
    else:
        product['name'] = name

    # @images
    images_list = []
    images_css = '#gal1 li'
    image_url_css = 'img::attr(src)'
    images = response.css(images_css)
    if (images == None):
        add_error('images', images_css, logs, file_path, actual_url)
    else:
        for i in range(0, len(images) - 1):
            # @image
            imageUrl = images[i].css(image_url_css).get()
            if (imageUrl == None):
                add_error('imageUrl', image_url_css, logs, file_path, actual_url)
            else:
                images_list.append(
                    imageUrl.replace('medium', 'large').replace('https://al-da.eu/', ''))
        product['images'] = str(images_list)

    # @description
    description_css = '.product-desc p'
    descriptions = response.css(description_css).get()
    description = ''
    for desc in descriptions:
        description = description + desc
    product['description'] = description.replace('<p>', '').replace(
        '</p>', '').replace('<br>', '').replace('</br>', '').replace('\xa0', '')

    # @size_table
    size_table_css = '.product-description table'
    size_table = response.css(size_table_css).get()
    product['size_table'] = size_table.replace('\n', '')

    # @color
    color_css = '.color .control-label .collapse.in span::text'
    color = response.css(color_css).get()
    if (color == None):
        d = product['description']
        product['color'] = d[d.find('kolor:') + 6:]
        pass
    else:
        product['color'] = color

    return product
