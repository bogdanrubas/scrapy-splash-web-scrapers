import os
from ..modules.logs.addLog import add_error

def get_all_categories(acceptable_categories_list, acceptable_sub_categories_list, response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.request.url
    categories_list = []
    categories_css = '.menu-desktop-content > ul > li'
    category_name_css = 'a::text'
    nested_categories_css = '.submenu-content > .submenu > .container > ul>li'
    nested_category_name_css = '::text'
    nested_category_url_css = 'a::attr(href)'
    categories = response.css(categories_css)

    if (categories == []):
        add_error('categories', categories_css, logs, file_path, actual_url)
    else:
        for category in categories:
            category_name = category.css(category_name_css).get()

            if category_name != None:
                if category_name in acceptable_categories_list:
                    nested_categories = category.css(nested_categories_css)
                    sub_cat=""
                    for nested_category in nested_categories:
                      buf = nested_category.css(
                          '.header-category').css('::text').get()
                      nested_category_name = nested_category.css(
                          nested_category_name_css).get()
                      if buf != None:
                        sub_cat = buf
                        continue
                      if sub_cat not in acceptable_sub_categories_list:
                        continue

                      nested_category_url = nested_category.css(
                          nested_category_url_css).get()
                      cat_name = category_name + '-/' + sub_cat + '-/' + nested_category_name

                      categories_list.append({
                          'name': cat_name,
                          'url': nested_category_url
                      })
                else:
                  print('category_name is not in acceptable_categories_list!!!')

    return(categories_list)
