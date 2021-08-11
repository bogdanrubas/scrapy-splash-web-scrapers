import os
from ..modules.logs.addLog import add_error

# categories_list: [{
# - name: string
# - url: string
# }]


def get_categories(self, response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.request.url

    categories_list = []
    categories_css = '#left_menu .bold'
    category_name_css = 'a::text'
    category_name_acceptable = ["KOBIETA", 'OUTLET']
    category_name_exception = [""]
    category_url_css = 'a::attr(href)'
    categories = response.css(categories_css)

    if (categories == []):
        add_error('categories', categories_css, logs, file_path, actual_url)
    else:
        for category in categories:
            # @category_name
            category_name = category.css(category_name_css).get()
            if (category_name == None):
                add_error('category_name', category_name_css,
                         logs, file_path, actual_url)
            else:
                if (len(category_name_acceptable) != 0):
                    if (category_name.strip() in category_name_acceptable
                            and category_name.strip() not in category_name_exception):
                        # @category_url
                        category_url = category.css(category_url_css).get()
                        if (category_url == None):
                            add_error('category_url', category_url_css,
                                     logs, file_path, actual_url)
                        else:
                            categories_list.append({
                                'name': category_name,
                                'url': category_url
                            })
                else:
                    if (category_name.strip() not in category_name_exception):
                        # @category_url
                        category_url = category.css(category_url_css).get()
                        if (category_url == None):
                            add_error('category_url', category_url_css,
                                     logs, file_path, actual_url)
                        else:
                            categories_list.append({
                                'name': category_name,
                                'url': category_url
                            })
    return(categories_list)
