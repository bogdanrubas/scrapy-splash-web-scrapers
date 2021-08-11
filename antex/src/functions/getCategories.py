import os
from ..modules.logs.addLog import add_error

# categories_list: [
# {
# - name: string
# - url: string
# },
# {
# - name: string
# - sub_categories: [
# - {
# - - name: string
# - - url: string
# - },
# - {
# - - name: string,
# - - sub_categories: [
# - - - name: string
# - - - url: string
# - - ]
# - }
# - ]
# },
#
# ]

def get_categories(self, response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.request.url

    categories_list = []
    #
    categories_css = '.mm_menus_ul > .mm_menus_li'
    category_name_css = 'a span::text'
    category_url_css = 'a::attr(href)'
    #
    sub_categories_css = 'ul .ets_mm_categories > li'
    sub_category_name_css = 'a::text'
    sub_category_url_css = 'a::attr(href)'
    #
    sub_sub_categories_css = 'ul > li'
    sub_sub_category_name_css = 'a::text'
    sub_sub_category_url_css = 'a::attr(href)'
    categories = response.css(categories_css)

    if (categories == []):
        add_error('categories', categories_css, logs, file_path, actual_url)
    else:
        for category in categories:
            sub_categories_list = []
            category_name = category.css(category_name_css).get()
            if (category_name == None):
                add_error('category_name', category_name_css,
                         logs, file_path, actual_url)
            else:
                sub_categories = category.css(sub_categories_css)

                if (sub_categories == []):
                    category_url = category.css(category_url_css).get()

                    if (category_url == None):
                        add_error('category_url', category_url_css,
                                 logs, file_path, actual_url)
                    else:
                        categories_list.append({
                            'name': (category_name[0:category_name.find(' (')].strip()),
                            'url': category_url
                        })
                else:
                    for sub_category in sub_categories:
                        sub_sub_categories_list = []
                        sub_category_name = sub_category.css(
                            sub_category_name_css).get()

                        if (sub_category_name == None):
                            add_error('sub_category_name', sub_category_name_css,
                                     logs, file_path, actual_url)
                        else:
                            sub_sub_categories = sub_category.css(
                                sub_sub_categories_css)

                            if (sub_sub_categories == []):
                                sub_category_url = sub_category.css(
                                    sub_category_url_css).get()

                                if (sub_category_url == None):
                                    add_error('sub_category_url', sub_category_url_css,
                                             logs, file_path, actual_url)
                                else:
                                    sub_categories_list.append({
                                        'name': sub_category_name[0:sub_category_name.find(' (')],
                                        'url': sub_category_url
                                    })
                            else:
                                for sub_sub_category in sub_sub_categories:
                                    sub_sub_category_name = sub_sub_category.css(
                                        sub_sub_category_name_css).get()

                                    if (sub_sub_category_name == None):
                                        add_error('sub_sub_category_name', sub_sub_category_name_css,
                                                 logs, file_path, actual_url)
                                    else:
                                        sub_sub_category_url = sub_sub_category.css(
                                            sub_sub_category_url_css).get()

                                        if (sub_sub_category_url == None):
                                            add_error('sub_sub_category_url', sub_sub_category_url_css,
                                                     logs, file_path, actual_url)
                                        else:
                                            sub_sub_categories_list.append({
                                                'name': sub_sub_category_name[0:sub_sub_category_name.find(' (')],
                                                'url': sub_sub_category_url
                                            })
                                sub_categories_list.append({
                                    'name': sub_category_name[0:sub_category_name.find(' (')],
                                    'sub_categories': sub_sub_categories_list
                                })
                    categories_list.append({
                        'name': (category_name[0:category_name.find(' (')]).strip(),
                        'sub_categories': sub_categories_list
                    })
    return(categories_list)
