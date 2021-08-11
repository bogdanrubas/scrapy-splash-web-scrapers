import os
from ..modules.logs.addLog import add_error

def get_all_categories(acceptable_categories_list, response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.request.url
    categories_list = []
    # najpierw zabiera główne kategorie
    categories_css = '.menu-ingrosso > li'
    category_name_css = 'a::text'
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
            if category_name != None:
                if category_name.lower() in acceptable_categories_list:
                    nested_categories = category.css(nested_categories_css)

                    for nested_category in nested_categories:
                        nested_category_name = nested_category.css(
                            nested_category_name_css).get()
                        nested_category_url = nested_category.css(
                            nested_category_url_css).get()
                        categories_list.append({
                            'name': nested_category_name,
                            'url': nested_category_url
                        })

    return(categories_list)
