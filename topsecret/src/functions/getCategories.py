import os
from ..modules.logs.addLog import add_error

# categories_list: [{
# - name: string
# - sub_categories: [
# - - name: string
# - - sub_categories: [
# - - - name: string
# - - - url: string (ex. /sub_sub_category-url)
# - - ]
# - ]
# }]


def get_categories(response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.request.url

    categories_list = []
    categories_css = '#menu > li'
    category_name_css = 'a::text'
    category_name_acceptable = ['ONA', 'ON', 'OUTLET']
    category_name_exception = ['']
    sub_categories_css = '.submenu > div > ul'
    sub_category_name_css = 'a::text'
    sub_category_name_acceptable = ["Odzież damska",
                                 "Akcesoria", "Odzież męska", "ONA", "ON"]
    sub_category_name_exception = []
    sub_sub_categories_css = 'li'
    sub_sub_category_name_css = 'a::text'
    sub_sub_category_name_acceptable = []
    sub_sub_category_name_exception = []
    sub_sub_category_url_css = 'a::attr(href)'

    categories = response.css(categories_css)

    if (categories == []):
        add_error('categories', categories_css, logs, file_path, actual_url)
    else:
        for category in categories:
            sub_categories_list = []
            category_name = category.css(category_name_css).get()
            print(f'category_name: {category_name}')
            if (category_name == None):
                add_error('category_name', category_name_css,
                         logs, file_path, actual_url)
            sub_categories = category.css(sub_categories_css)
            if (sub_categories == []):
                add_error('sub_categories', sub_categories_css,
                         logs, file_path, actual_url)
            else:
                for sub_category in sub_categories:
                    sub_sub_categories_list = []
                    sub_category_name = sub_category.css(sub_category_name_css).get()
                    print(f'sub_category_name: {sub_category_name}')
                    if (sub_category_name == None):
                        add_error('sub_category_name', sub_category_name_css,
                                 logs, file_path, actual_url)
                    sub_sub_categories = sub_category.css(sub_sub_categories_css)
                    if (sub_sub_categories == []):
                        add_error('sub_sub_categories', sub_sub_categories_css,
                                 logs, file_path, actual_url)
                    else:
                        for sub_sub_category in sub_sub_categories:
                            sub_sub_category_name = sub_sub_category.css(
                                sub_sub_category_name_css).get()
                            if (sub_sub_category_name == None):
                                add_error(
                                    'sub_sub_category_name', sub_sub_category_name_css, logs, file_path, actual_url)
                            sub_sub_category_url = sub_sub_category.css(
                                sub_sub_category_url_css).get()
                            if (sub_sub_category_url == None):
                                add_error(
                                    'sub_sub_category_url', sub_sub_category_url_css, logs, file_path, actual_url)

                            if (len(sub_sub_category_name_acceptable) != 0):
                                if (sub_sub_category_name != None):
                                    if (sub_sub_category_name.strip() in sub_sub_category_name_acceptable
                                            and sub_sub_category_name.strip() not in sub_sub_category_name_exception):
                                        sub_sub_categories_list.append({
                                            'name': sub_sub_category_name,
                                            'url': sub_sub_category_url
                                        })
                            else:
                                if (sub_sub_category_name != None):
                                    if (sub_sub_category_name.strip() not in sub_sub_category_name_exception):
                                        sub_sub_categories_list.append({
                                            'name': sub_sub_category_name,
                                            'url': sub_sub_category_url
                                        })

                        if (len(sub_category_name_acceptable) != 0):
                            if (sub_category_name.strip() in sub_category_name_acceptable
                                    and sub_category_name.strip() not in sub_category_name_exception):
                                sub_categories_list.append({
                                    'name': sub_category_name,
                                    'subCategories': sub_sub_categories_list
                                })
                        else:
                            if (sub_category_name.strip() not in sub_category_name_exception):
                                sub_categories_list.append({
                                    'name': sub_category_name.strip(),
                                    'subCategories': sub_sub_categories_list
                                })

            if (len(category_name_acceptable) != 0):
                if (category_name.strip() in category_name_acceptable
                        and category_name.strip() not in category_name_exception):
                    categories_list.append({
                        'name': category_name.strip(),
                        'subCategories': sub_categories_list
                    })
            else:
                if (category_name.strip() not in category_name_exception):
                    categories_list.append({
                        'name': category_name.strip(),
                        'subCategories': sub_categories_list
                    })
    return(categories_list)
