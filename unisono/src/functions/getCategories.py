import os
from ..modules.logs.addLog import add_error

# categories_list: [{
# - name: string
# - subCategories: [
# - - name: string
# - - subCategories: [
# - - - name: string
# - - - url: string (ex. /subSubCategory-url)
# - - ]
# - ]
# }]


def get_categories(self, response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.request.url

    categories_list = []
    categoriesCss = '#menu > div > ul > li'
    category_name_css = 'a::text'
    sub_categories_css = '.submenu > ul > li'
    sub_category_name_css = 'a::text'
    sub_sub_categories_css = 'ul li'
    sub_sub_category_name_css = 'a::text'
    sub_sub_category_url_css = 'a::attr(href)'
    categories = response.css(categoriesCss)

    if (categories == []):
        add_error('categories', categoriesCss, logs, file_path, actual_url)
    else:
        for category in categories:
            sub_categories_list = []
            category_name = category.css(category_name_css).get()
            if (category_name == None):
                add_error('category_name', category_name_css,
                         logs, file_path, actual_url)
            sub_categories = category.css(sub_categories_css)
            if (sub_categories == []):
                add_error('sub_categories', sub_categories_css,
                         logs, file_path, actual_url)
            else:
                for subCategory in sub_categories:
                    sub_sub_categories_list = []
                    sub_category_name = subCategory.css(sub_category_name_css).get()
                    if (sub_category_name == None):
                        add_error('sub_category_name', sub_category_name_css,
                                 logs, file_path, actual_url)
                    sub_sub_categories = subCategory.css(sub_sub_categories_css)
                    if (sub_sub_categories == []):
                        # add_error('sub_sub_categories', sub_sub_categories_css,
                        #          logs, file_path, actual_url)
                        pass
                    else:
                        for subSubCategory in sub_sub_categories:
                            sub_sub_category_name = subSubCategory.css(
                                sub_sub_category_name_css).get()
                            if (sub_sub_category_name == None):
                                add_error(
                                    'sub_sub_category_name', sub_sub_category_name_css, logs, file_path, actual_url)
                            sub_sub_category_url = subSubCategory.css(
                                sub_sub_category_url_css).get()
                            if (sub_sub_category_url == None):
                                add_error(
                                    'sub_sub_category_url', sub_sub_category_url_css, logs, file_path, actual_url)
                            sub_sub_categories_list.append({
                                'name': sub_sub_category_name,
                                'url': sub_sub_category_url
                            })

                        if sub_category_name != "Najczęściej wybierane" and sub_category_name != "Polecane kategorie":
                            sub_categories_list.append({
                                'name': sub_category_name,
                                'subCategories': sub_sub_categories_list
                            })

            categories_list.append({
                'name': category_name,
                'subCategories': sub_categories_list
            })
    return(categories_list)
