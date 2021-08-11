import os
from ..modules.logs.addLog import add_error

def get_data(response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.url

    product = {
        'url': '',
        'available': True,
        'category': '',
        'name': '',
        'new_price': 0,
        'old_price': 0,
        'images': [],
        'description': '',
        'sizes': [],
        'colors': []
    }
    product['url'] = actual_url
    product['category'] = response.meta.get('category')

    # @name
    name_css = 'h1.product_title::text'
    name = response.css(name_css).get()
    if (name == None):
        add_error('name', name_css, logs, file_path, actual_url)
    else:
        product['name'] = name

    # @images
    images_list = []
    images_css = '.slick-track > div'
    image_ulr_css = 'img::attr(src)'
    images = response.css(images_css)
    if (images == None):
        add_error('images', images_css, logs, file_path, actual_url)
    else:
        for image in images:
            # @image
            imageUrl = image.css(image_ulr_css).get()
            if (imageUrl == None):
                add_error('imageUrl', image_ulr_css, logs, file_path, actual_url)
            else:
                images_list.append(imageUrl.replace(
                    '-150x150', '').replace('-595x893', ''))
        product['images'] = images_list

    # @sizes & @color
    sizes_list = []
    colors_list = []
    product_css = '.product-page > .product'

    product_container = response.css(product_css)

    if product_container != None:
        classses = (product_container.css('::attr(class)').get()).split()

        for cl in classses:
            # @ sizes
            if cl.find('rozmiar') != -1:
                size = cl.replace('pa_rozmiar-', '')
                sizes_list.append(size)
            if cl.find('kolor') != -1:
                color = cl.replace('pa_kolor-', '')
                colors_list.append(color)
    else:
        add_error('product', product_css, logs, file_path, actual_url)
    product['sizes'] = sizes_list
    product['colors'] = colors_list

    # @description

    description_p_css = '.woocommerce-product-details__short-description p'

    description_p = response.css(description_p_css)
    description = ''

    for i in range(0, len(description_p)):
        if i < len(description_p) - 2:
            desc_text = description_p[i].css('::text').get()
            description = description + ' ' + desc_text

    product['description'] = description

    # @price
    new_price_css = '.nasa-single-product-slide > .row ins span::text'
    old_price_css = '.nasa-single-product-slide > .row del span::text'

    price = response.css(new_price_css).get()
    if price == None:
        pass
        # bez promocji
    else:
        new_price = response.css(new_price_css).get()
        old_price = response.css(old_price_css).get()
        product['old_price'] = float(old_price.replace(',', '.'))
        product['new_price'] = float(new_price.replace(',', '.'))

    # @available

    available_css = 'div.row.nasa-product-details-page > div.large-9.columns.right.nasa-single-product-slide > div.row > div.large-6.small-12.columns.product-info.summary.entry-summary.left.rtl-left > form > div > div.woocommerce-variation.single_variation > div.woocommerce-variation-availability > p'
    available = response.css(available_css)

    if available != []:
        product['available'] = False

    return product
