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
# }


def get_product(self, response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]

    actual_url = response.meta.get('actual_url')
    product = {}
    product['url'] = response.meta.get('actual_url')
    product['category'] = response.meta.get('category')
    product['sub_category'] = response.meta.get('sub_category')
    product['sub_sub_category'] = response.meta.get('sub_sub_category')
    product['artykul'] = ''
    product['name'] = ''
    product['color'] = ''
    product['new_price'] = 0
    product['old_price'] = 0
    product['sizes'] = [{
        'name': '',
        'quantity': 0
    }]
    product['images'] = [""]

    # @id:
    id_css = '.product-data .product-nb::text'
    id = response.css(id_css).get()
    if(id == None):
        add_error('id', id_css, logs, file_path, actual_url)
    else:
        product['artykul'] = id.replace("art: ", "")[
            0:id.replace("art: ", "").find(" ")]

    # @color
    color_css = 'tr:nth-child(1) .desc_right_td::text'
    color = response.css(color_css).get()
    if (color == None):
        add_error('color', color_css, logs, file_path, actual_url)
    else:
        product['color'] = color

    # @name
    name_css = '.product-data-name::text'
    name = response.css(name_css).get()
    if (name == None):
        add_error('name', name_css, logs, file_path, actual_url)
    else:
        product['name'] = name.strip()

    # @description
    # artykul + name <br>
    ## details + description
    description_text = ''
    details_text = ''

    # description
    description_css = '.product-desc .text::text'
    description = response.css(description_css).get()
    if (description == None):
        pass
    else:
        description_text = description.strip().replace("\r\n", "")

    # details
    details_css = '.product-detalis table'
    details = response.css(details_css).get()
    if (details == None):
        add_error('details', details_css, logs, file_path, actual_url)
    else:
        details_text = details.strip().replace(
            "\r", "").replace("\n", "").replace("\t", "")

    product['description'] = product['artykul'] + \
        product['name'] + "<br>" + details_text + description_text

    # @new_price
    new_price_css = '.price-new::text'
    new_price = response.css(new_price_css).get()
    if (new_price == None):
        add_error('new_price', new_price_css, logs, file_path, actual_url)
    else:
        product['new_price'] = float(
            new_price.strip().replace(" ", "").replace(",", "."))

    # @old_price
    old_price_css = '.price-old::text'
    old_price = response.css(old_price_css).get()
    if (old_price == None):
        product['old_price'] = product['new_price']
    else:
        product['old_price'] = float(
            old_price.strip().replace(" ", "").replace(",", "."))

    # @sizes
    sizes_list = []
    sizes_css = '.variants li'
    size_name_css = 'a::text'
    size_quantity_css = '::attr(data-quant)'
    sizes = response.css(sizes_css)
    if (sizes == []):
        # add_error('sizes', sizes_css, logs, file_path, actual_url)
        pass
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

    # @images
    images_list = []
    images_css = '#small-photo a'
    image_css = '::attr(href)'
    images = response.css(images_css)
    if (images == []):
        add_error('images', images_css, logs, file_path, actual_url)
    else:
        for image in images:
            # @image
            url = image.css(image_css).get()
            if (url == None):
                add_error('image', image_css, logs, file_path, actual_url)
            else:
                images_list.append(url)
        product['images'] = images_list
    return product
