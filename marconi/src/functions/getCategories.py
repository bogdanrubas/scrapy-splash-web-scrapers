import os
from ..modules.logs.addLog import add_error


def get_categories(response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.request.url
    s0_categories_list = []

    s0_categories_css = '.menu-content > li'
    s0_category_name_css = 'a::text'
    s0_category_url_css = 'a::attr(href)'
    s0_category_name_acceptable = []
    s0_category_name_exception = [
        'Outlet', 'Sklep stacjonarny', 'Akcesoria']

    s1_categories_xpath = './ul/li'
    s1_category_name_css = 'a::text'
    s1_category_url_css = 'a::attr(href)'
    s1_category_name_acceptable = []
    s1_category_name_exception = []

    s2_categories_css = 'ul > li'
    s2_category_name_css = 'a::text'
    s2_category_url_css = 'a::attr(href)'
    s2_category_name_acceptable = []
    s2_category_name_exception = []

    categories = response.css(s0_categories_css)

    if (categories == []):
        add_error('categories', s0_categories_css, logs, file_path, actual_url)
    else:
        for category in categories:
            s1_categories_list = []
            categoryName = category.css(s0_category_name_css).get()
            if (categoryName == None):
                add_error('categoryName', s0_category_name_css,
                         logs, file_path, actual_url)
            categoryUrl = category.css(s0_category_url_css).get()
            if (categoryUrl == None):
                add_error('categoryUrl', s0_category_url_css,
                         logs, file_path, actual_url)
            s1_categories = category.xpath(s1_categories_xpath)
            if (s1_categories == []):
                s0_categories_list.append({
                    'name': categoryName,
                    'url': categoryUrl
                })
            else:
                for s1_category in s1_categories:
                    sub_sub_categories_list = []
                    s1_category_name = s1_category.css(s1_category_name_css).get()
                    if (s1_category_name == None):
                        add_error('s1_category_name', s1_category_name_css,
                                 logs, file_path, actual_url)
                    s1_category_url = s1_category.css(s1_category_url_css).get()
                    if (s1_category_url == None):
                        add_error('s1_category_url', s1_category_url_css,
                                 logs, file_path, actual_url)
                    s2_categories = s1_category.css(s2_categories_css)
                    if (s2_categories == [] and s1_category_name != None):
                        # ? and poniewaz jeden li zawiera obrazek a nie link
                        s1_categories_list.append({
                            'name': s1_category_name,
                            'url': s1_category_url,
                        })
                    else:
                        for s2_category in s2_categories:
                            s2_category_name = s2_category.css(
                                s2_category_name_css).get()
                            if (s2_category_name == None):
                                add_error(
                                    's2_category_name', s2_category_name_css, logs, file_path, actual_url)
                            s2_category_url = s2_category.css(
                                s2_category_url_css).get()
                            if (s2_category_url == None):
                                add_error(
                                    's2_category_url', s2_category_url_css, logs, file_path, actual_url)

                            if (len(s2_category_name_acceptable) != 0):
                                if (s2_category_name.strip() in s2_category_name_acceptable
                                        and s2_category_name.strip() not in s2_category_name_exception):
                                    sub_sub_categories_list.append({
                                        'name': s2_category_name,
                                        'url': s2_category_url
                                    })
                            else:
                                if (s2_category_name.strip() not in s2_category_name_exception):
                                    sub_sub_categories_list.append({
                                        'name': s2_category_name,
                                        'url': s2_category_url
                                    })

                    if s2_categories != []:
                        if (len(s1_category_name_acceptable) != 0):
                            if (s1_category_name.strip() in s1_category_name_acceptable
                                    and s1_category_name.strip() not in s1_category_name_exception):
                                s1_categories_list.append({
                                    'name': s1_category_name,
                                    'subCategories': sub_sub_categories_list
                                })
                        else:
                            if (s1_category_name.strip() not in s1_category_name_exception):
                                s1_categories_list.append({
                                    'name': s1_category_name.strip(),
                                    'subCategories': sub_sub_categories_list
                                })

            if s1_categories != []:
                if (len(s0_category_name_acceptable) != 0):
                    if (categoryName.strip() in s0_category_name_acceptable
                            and categoryName.strip() not in s0_category_name_exception):
                        s0_categories_list.append({
                            'name': categoryName.strip(),
                            'subCategories': s1_categories_list
                        })
                else:
                    if (categoryName.strip() not in s0_category_name_exception):
                        s0_categories_list.append({
                            'name': categoryName.strip(),
                            'subCategories': s1_categories_list
                        })
    return(s0_categories_list)
