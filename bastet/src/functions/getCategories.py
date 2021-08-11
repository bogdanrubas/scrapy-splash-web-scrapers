import os
from ..modules.logs.addLog import add_error


def get_categories(response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.request.url
    categories_list = []

    categories_css = '#site-navigation > li'
    category_name_css = 'a span::text'
    sub_categories_css = 'div > ul > li'
    sub_category_name_css = 'a span::text'
    sub_category_url_css = 'a::attr(href)'

    categories = response.css(categories_css)

    if (categories == []):
        add_error('categories', categories_css, logs, file_path, actual_url)
    else:
        for category in categories:
            categoryname = category.css(category_name_css).get()

            if categoryname.lower() == 'kolekcja':
                subCategories = category.css(sub_categories_css)

                if subCategories == []:
                    add_error('subCategories', sub_categories_css,
                             logs, file_path, actual_url)
                else:
                    for subCategory in subCategories:
                        name = subCategory.css(sub_category_name_css).get()
                        url = subCategory.css(sub_category_url_css).get()

                        categories_list.append({
                            'name': name,
                            'url': url
                        })
    return(categories_list)
