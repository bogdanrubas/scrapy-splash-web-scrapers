import os
from ..modules.logs.addLog import add_error

# product: {
# - url: string
# - category: string
# - sub_category: string
# - sub_sub_category: string
# - artykul: string
# - name: string
# - color: string
# - new_price: float
# - old_price: float
# - sizes: [
# - - name: string
# - - available: boolean
# - ]
# - images: string[]
# - description: string
# - sizes_table: string
# }


def clear_price(price):
    if price == None:
        return 0
    else:
        modifed_price = float(price.strip().replace(
            ",", ".").replace("PLN", "").replace("\xa0", "").replace(" ", ""))
        return modifed_price


def get_data(response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.meta.get('actual_url')

    product = {
        'url': '',
        'category': '',
        'sub_category': '',
        'sub_sub_category': '',
        'artykul': '',
        'name': '',
        'new_price': 0,
        'old_price': 0,
        'color': '',
        'sizes': '',
        'images': '',
        'description': '',
        'sizes_table': ''
    }
    product['url'] = actual_url
    product['category'] = response.meta.get('category')
    product['sub_category'] = response.meta.get('sub_category')
    product['sub_sub_category'] = response.meta.get('sub_sub_category')

    # @artykul
    artykul_css = '.markname-safo span:last-of-type::text'
    artykul = response.css(artykul_css).get()
    if (artykul == None):
        add_error('artykul', artykul_css, logs, file_path, actual_url)
    else:
        product['artykul'] = artykul.replace(" | ", "")

    # @name
    name_css = '.container .name::text'
    name = response.css(name_css).get()
    if (name == None):
        add_error('name', name_css, logs, file_path, actual_url)
    else:
        product['name'] = name

    # @new_price & @old_price:
    # ? sprawdzanie czy jest promocja czy regularna cena
    regular_price = response.css('span.price-regular::text').get()
    if (regular_price == None):
        # jesli promocja:
        old_price_css = '.price-old span::text'
        old_price = response.css(old_price_css).get()
        if (old_price == None):
            add_error('old_price', old_price_css, logs, file_path, actual_url)
        else:
            product['old_price'] = clear_price(old_price)

        new_price_css = '.price-promo'
        new_price = response.css(new_price_css)
        if (new_price == []):
            add_error('new_price', new_price_css, logs, file_path, actual_url)
        else:
            if (new_price.css('span').get() == None):
                product['new_price'] = clear_price(new_price.css('::text').get())
            else:
                n_price = new_price.css('span::text').get()
                product['new_price'] = clear_price(n_price)
    else:
        # jesli nie ma promocji:
        product['old_price'] = clear_price(regular_price)
        product['new_price'] = clear_price(regular_price)

    color_css = '.colors span::text'
    color = response.css(color_css).get()
    if (color == None):
        add_error('color', color_css, logs, file_path, actual_url)
    else:
        product['color'] = color

    # @sizes
    sizes_list = []
    sizes_css = '.sizes > ul > li > div'
    size_name_css = '::text'
    sizes = response.css(sizes_css)
    if (sizes == None):
        add_error('sizes', sizes_css, logs, file_path, actual_url)
    else:
        for size in sizes:
            size_data = {}
            # @size_name
            size_name = size.css(size_name_css).get()
            if (size_name == None):
                add_error('size_name', size_name_css, logs, file_path, actual_url)
            else:
                size_data['name'] = size_name
                # @sizeAvailable
                classes = size.css('::attr(class)').get()
                if (classes.find('unavailable') == -1):
                    size_data['available'] = True
                else:
                    size_data['available'] = False
            sizes_list.append(size_data)
        product['sizes'] = sizes_list

    # @images
    images_list = []
    images_css = '#thumbails-slider li'
    image_url_css = 'img::attr(src)'
    images = response.css(images_css)
    if (images == None):
        add_error('images', images_css, logs, file_path, actual_url)
    else:
        for image in images:
            # @image
            image_url = image.css(image_url_css).get()
            if (image_url == None):
                add_error('image_url', image_url_css, logs, file_path, actual_url)
            else:
                images_list.append(image_url.replace("/thumb_104x139", ""))
        product['images'] = images_list

    # @description
    accordion_lis_css = '.accordion ul > li'
    accordion_lis = response.css(accordion_lis_css)
    if (accordion_lis == []):
        pass
    else:
        product['description'] = accordion_lis[0].css(
            'p:last-of-type').get().replace('<p itemprop="description">', '').replace('</p>', '').strip()

    # @sizes_table
    sizes_table_css = '.sizesScroll table'
    sizes_table = response.css(sizes_table_css).get()
    if (sizes_table == None):
        add_error('sizes_table', sizes_table_css, logs, file_path, actual_url)
    else:
        product['sizes_table'] = sizes_table.strip().replace(
            '\n', '').replace("  ", "")

    return product
