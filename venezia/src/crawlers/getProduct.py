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
# - - quantity: int
# - ]
# - images: string[]
# - description: string
# - description_table: string
# }


def get_product(self, response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.meta.get('actual_url')
    product = {}
    product['artykul'] = ''
    product['url'] = actual_url
    product['category'] = response.meta.get('category')
    product['sub_category'] = response.meta.get('sub_category')
    product['sub_sub_category'] = response.meta.get('sub_sub_category')

    # @artykul
    artykul_css = '.catalog_number_header::text'
    artykul = response.css(artykul_css).get()

    if (artykul == None):
        add_error('artykul', artykul_css, logs, file_path, actual_url)
    else:
        product['artykul'] = artykul.replace("art.: ", "")

    # @name
    name_css = '.product_name::text'
    name = response.css(name_css).get()

    if (name == []):
        add_error('name', name_css, logs, file_path, actual_url)
    else:
        product['name'] = name.strip()

    # @new_price
    new_price_css = '#price::text'
    new_price = response.css(new_price_css).get()

    if (new_price == None):
        add_error('new_price', new_price_css, logs, file_path, actual_url)
    else:
        product['new_price'] = float(new_price.strip())

    # @old_price
    old_price_css = '.price_box_old span::text'
    old_price = response.css(old_price_css).get()

    if (old_price == None):
        product['old_price'] = float(new_price.strip())
    else:
        product['old_price'] = float(old_price.strip())

    # @sizes
    sizes_list = []
    sizes_css = '.sizes > .size'
    size_name_css = '::text'
    size_quantity_css = '::attr(data-quant)'
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
            # @size_quantity
            size_quantity = size.css(size_quantity_css).get()
            if (size_quantity == None):
                add_error('size_quantity', size_quantity_css,
                         logs, file_path, actual_url)
            else:
                size_data['quantity'] = size_quantity

            sizes_list.append(size_data)
        product['sizes'] = sizes_list

    # @color
    color_trs_css = '.product_description tr'
    left_column_css = '.desc_left_td span::text'
    right_column_css = '.desc_right_td::text'
    color = ''
    color_trs = response.css(color_trs_css)

    if (color_trs == None):
        add_error('color', color_trs_css, logs, file_path, actual_url)
    else:
        for tr in color_trs:
            if tr.css(left_column_css).get() != None:
                if tr.css(left_column_css).get().strip() == 'Kolor:':
                    color = tr.css(right_column_css).get().strip()
    product['color'] = color

    # @images
    images_list = []
    images_css = '.product_images img'
    image_css = '::attr(src)'
    #imagePropertyCss = ''
    images = response.css(images_css)

    if (images == None):
        add_error('images', images_css, logs, file_path, actual_url)
    else:
        for image in images:
            # @image
            url = image.css(image_css).get()
            if (image == None):
                add_error('image', image_css, logs, file_path, actual_url)
            else:
                url = url.replace('_mini', '')
                images_list.append(url)
        product['images'] = images_list

    # @description
    # ? scala kilka divów w jeden string, usuwa puste divy
    description_css = '.text_info div'
    description = response.css(description_css)
    description_text = ''

    if (description == None):
        add_error('description', description_css, logs, file_path, actual_url)
    else:
        for div in description:
            if (div.css('::text').get() != None):
                description_text += div.css('::text').get()
        product['description'] = description_text

    # @description_table
    # ? sprawdza czy istnieje tablica, jesli istnieje to
    # ? zbiera tekst ze wszystkich td i tworzy nową tablicę
    # ? aby pozbyć się niepotrzebnych tagów ze strony
    description_table_css = '.product_description > table'
    description_table_trs_css = '.product_description tr'
    description_table_html = ''
    description_table = response.css(description_table_css).get()

    if (description_table == None):
        add_error('description_table', description_table_css,
                 logs, file_path, actual_url)
    else:
        description_table_trs = response.css(description_table_trs_css)
        description_table_trs_html = ''

        for tr in description_table_trs:
            left_column_text = tr.css('::text').get().strip()
            right_column_text = tr.css('td::text').get()

            # ? kiedy jest tylko jedno td w tr:
            if (left_column_text == right_column_text):
                tr_element = f'<tr><td>{left_column_text}</td>/tr>'
            else:
                tr_element = f'<tr><td>{left_column_text}</td><td>{right_column_text}</td></tr>'

            if (left_column_text != ''):
                description_table_trs_html += tr_element
        description_table_html = f'<table><tbody>{description_table_trs_html}</tbody></table>'
        product['description_table'] = description_table_html
    return product
