import os
from ...modules.logs.addLog import add_error

def get_all_categories(not_acceptable_categories, response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.request.url
    categories_list = []
    # najpierw zabiera główne kategorie
    categories_css = 'body > div > table > tbody > tr > td > table:nth-child(2) > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(1) > td > table.infoBox > tbody > tr > td > table > tbody > tr:nth-child(2) > td > p > a'
    category_name_css = '::text'
    category_url_css = '::attr(href)'
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

            if (category_name.lower() not in not_acceptable_categories) and (category_element not in categories_list):
                categories_list.append({
                    'name': category_name,
                    'url': category_url
                })

    return(categories_list)
