import os
from ..modules.logs.addLog import add_error

# sub_categories_list: [{
# - name: string
# - url: string
# }]


def get_rest_of_categories(self, response, logs, categoryName):
    lis_css = '#left_menu li'
    li_classes_css = '::attr(class)'
    sub_category_name_css = '::text'
    sub_sub_category_name_css = 'a::text'
    sub_sub_category_url_css = 'a::attr(href)'
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.request.url
    sub_categories_list = []
    lis = response.css(lis_css)
    woman_sub_category_name_index = 0
    man_sub_category_name_index = 0

    if categoryName == 'OUTLET':
        if (lis == []):
            add_error('lis', lis_css, logs, file_path, actual_url)
        else:
            for li in lis:
                li_classes = li.css(li_classes_css).get()

                # znalezienie z ktorej pozycji zaczynaja sie subsub_categories dla
                # Kolekcja Damska i Kolekcja Męska
                # oraz dodanie {
                # name: 'Kolekcja Damska',
                # sub_categories: []
                # } i {
                # name: 'Kolekcja Męska',
                # sub_categories: []
                # } do sub_categories_list
                if (li_classes == 'bold' or li_classes == 'bold current' or li_classes == 'bold '):
                    sub_category_name = li.css(sub_category_name_css).get()

                    if (sub_category_name == None):
                        add_error('sub_category_name', sub_category_name_css,
                                 logs, file_path, actual_url)
                    else:
                        if (sub_category_name.find('KOBIETA') != -1):
                            sub_categories_list.append({
                                'name': 'Kolekcja Damska',
                                'sub_categories': []
                            })
                            woman_sub_category_name_index = lis.index(li)
                        elif (sub_category_name.find('MĘŻCZYZNA') != -1):
                            sub_categories_list.append({
                                'name': 'Kolekcja Męska',
                                'sub_categories': []
                            })
                            man_sub_category_name_index = lis.index(li)

            woman_list = []
            man_list = []

            for li in lis:
                if (lis.index(li) > woman_sub_category_name_index
                        and lis.index(li) < man_sub_category_name_index):
                    sub_sub_category = {
                        'name': '',
                        'url': ''
                    }

                    # @sub_sub_category_name
                    sub_sub_category_name = li.css(sub_sub_category_name_css).get()
                    if (sub_sub_category_name == None):
                        add_error('sub_sub_category_name', sub_sub_category_name_css,
                                 logs, file_path, actual_url)
                    else:
                        sub_sub_category['name'] = sub_sub_category_name

                    # @sub_sub_category_url
                    sub_sub_category_url = li.css(sub_sub_category_url_css).get()
                    if (sub_sub_category_url == None):
                        add_error('sub_sub_category_url', sub_sub_category_url_css,
                                 logs, file_path, actual_url)
                    else:
                        sub_sub_category['url'] = sub_sub_category_url

                    woman_list.append(sub_sub_category)
                elif (lis.index(li) > man_sub_category_name_index):
                    li_classes = li.css(li_classes_css).get()

                    if li_classes == None:
                        sub_sub_category = {
                            'name': '',
                            'url': ''
                        }

                        # @sub_sub_category_name
                        sub_sub_category_name = li.css(
                            sub_sub_category_name_css).get()
                        if (sub_sub_category_name == None):
                            add_error('sub_sub_category_name', sub_sub_category_name_css,
                                     logs, file_path, actual_url)
                        else:
                            sub_sub_category['name'] = sub_sub_category_name

                        # @sub_sub_category_url
                        sub_sub_category_url = li.css(sub_sub_category_url_css).get()
                        if (sub_sub_category_url == None):
                            add_error('sub_sub_category_url', sub_sub_category_url_css,
                                     logs, file_path, actual_url)
                        else:
                            sub_sub_category['url'] = sub_sub_category_url

                        man_list.append(sub_sub_category)
                sub_categories_list[0]['sub_categories'] = woman_list
                sub_categories_list[1]['sub_categories'] = man_list
    else:
        if (lis == []):
            add_error('lis', lis_css, logs, file_path, actual_url)
        else:
            for li in lis:
                li_classes = li.css(li_classes_css).get()
                if li_classes == None:
                    sub_categories_list.append({
                        'name': li.css(sub_category_name_css).get(),
                        'url': li.css(sub_sub_category_url_css).get()
                    })
    return(sub_categories_list)
