import os
from ..modules.logs.addLog import add_error

# product: {
# - url: string
# - s0_category: string
# - s1_category: string
# - s2_category: string
# - name: string
# - price: float
# - sizes: string[]
# - images: string[]
# - description: string
# }

def get_data(response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.url

    product = {
        'url': '',
        's0_category': '',
        's1_category': '',
        's2_category': '',
        'name': '',
        'price': 0,
        'description': '',
        'images': '',
        'detals': '',
        'sizes': '',
    }
    product['url'] = actual_url
    product['s0_category'] = response.meta.get('s0_category')
    product['s1_category'] = response.meta.get('s1_category')
    product['s2_category'] = response.meta.get('s2_category')

    # @name
    name_css = 'h1::text'
    name = response.css(name_css).get()
    if (name == None):
        add_error('name', name_css, logs, file_path, actual_url)
    else:
        product['name'] = name

    # @price
    price_css = '#our_price_display::text'
    price = response.css(price_css).get()
    if (price == None):
        add_error('price', price_css, logs, file_path, actual_url)
    else:
        product['price'] = float(price.replace('zł', '').replace(' ', ''))

    # @description
    description_css = '#short_description_content p::text'
    description = response.css(description_css).get()
    if (description == None):
        add_error('description', description_css, logs, file_path, actual_url)
    else:
        product['description'] = description

    # @images
    images_list = []
    image_css = '#thumbs_list_frame li'
    image_url_css = 'a::attr(href)'
    images = response.css(image_css)
    if (images == None):
        add_error('images', image_css, logs, file_path, actual_url)
    else:
        for image in images:
            # @image
            image_url = image.css(image_url_css).get()
            if (image_url == None):
                add_error('image_url', image_url_css, logs, file_path, actual_url)
            else:
                images_list.append(image_url)
        product['images'] = str(images_list)

    # @detals
    detals_list = []
    detals_css = '#detal table tr'
    detals = response.css(detals_css)
    if (detals == None):
        add_error('detals', detals_css, logs, file_path, actual_url)
    else:
        for detal in detals:
            detal_name = detal.css('td:first-of-type::text').get()
            detal_value = detal.css('td:last-of-type::text').get()
            detals_list.append({
                'name': detal_name.replace(':', ''),
                'value': detal_value
            })
    product['detals'] = str(detals_list)

    # @sizes
    sizes_list = []
    fieldsets_css = '#attributes fieldset'
    label_css = 'label::text'
    sizes_css = 'select > option'
    size_name_css = '::attr(title)'
    fieldsets = response.css(fieldsets_css)

    for fieldset in fieldsets:
        labelText = fieldset.css(label_css).get()
        if labelText.lower().find('rozmiar') != -1:
            sizes = fieldset.css(sizes_css)
            if sizes == []:
                add_error('sizes', sizes_css, logs, file_path, actual_url)
            else:
                for size in sizes:
                    sizeName = size.css(size_name_css).get()
                    if sizeName == None:
                        add_error('sizeName', size_name_css,
                                 logs, file_path, actual_url)
                    else:
                        sizes_list.append(sizeName)
    product['sizes'] = str(sizes_list)

    return product
