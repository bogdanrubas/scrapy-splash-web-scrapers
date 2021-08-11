import os
from ..modules.logs.addLog import add_error

def get_categories(response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.request.url
    categories_list = []
    categories_css = '.jms-megamenu > ul > li'
    category_name_css = 'a > span::text'
    category_url_css = 'a::attr(href)'
    acceptable_categories = [
      # 'sukienki', 'bluzki', 'bolerka i marynarki', 'spódnice', 'kurtki i płaszcze'
      'dresses',
      'blouses',
      'boleros & jackets'
      'skirts'
      ]
    categories = response.css(categories_css)

    if (categories == []):
        add_error('categories', categories_css, logs, file_path, actual_url)
    else:
        for category in categories:
            category_name = category.css(category_name_css).get()
            print(category_name)

            if category_name.lower() in acceptable_categories:
                url = category.css(category_url_css).get()
                categories_list.append({
                    'name': category_name,
                    'url': url
                })
    return(categories_list)
