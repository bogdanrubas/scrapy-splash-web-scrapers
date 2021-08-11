import os
from ..modules.logs.addLog import add_error


def get_all_categories(not_acceptable_categories, response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.request.url
    categories_list = []
    # najpierw zabiera główne kategorie
    categories_css = '.widget_product_categories ul.product-categories > li'
    category_name_css = 'a::text'
    category_url_css = 'a::attr(href)'
    # później zabiera zagniezdzone kategorie
    nested_categories_css = 'ul > li'
    nested_category_name_css = 'a::text'
    nested_category_url_css = 'a::attr(href)'

    categories = response.css(categories_css)

    if (categories == []):
        add_error('categories', categories_css, logs, file_path, actual_url)
    else:
        for category in categories:
            category_name = category.css(category_name_css).get()
            category_url = category.css(category_url_css).get()
            category_element = {
                'name': category_name,
                'url': category_url
            }
            nested_categories = category.css(nested_categories_css)

            if (category_name.lower() not in not_acceptable_categories) and (category_element not in categories_list):
                categories_list.append({
                    'name': category_name,
                    'url': category_url
                })

            if nested_categories == []:
                pass
            else:
                for nested_category in nested_categories:
                    nested_category_name = nested_category.css(
                        nested_category_name_css).get()
                    nested_category_url = nested_category.css(
                        nested_category_url_css).get()
                    nested_category_element = {
                        'name': nested_category_name,
                        'url': nested_category_url
                    }

                    if (nested_category_name not in not_acceptable_categories) and (nested_category_element not in categories_list):
                        categories_list.append({
                            'name': nested_category_name,
                            'url': nested_category_url
                        })

    return(categories_list)
