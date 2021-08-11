import os
from ..modules.logs.addLog import add_error
import json

# pages_list: string[] (ex. https://example.com/page1


def get_pages(response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.meta.get('actual_url')

    # @pages
    pages_list = []
    meta_data_css = '#product-list::attr(data-init-navigation)'
    page_suffix = '?sort=sorting_by_add_date_desc&pageno='

    meta_data = response.css(meta_data_css).get()

    if (meta_data == None):
        add_error('', meta_data_css, logs, file_path, actual_url)
    else:
        jsonData = json.loads(meta_data)
        if (jsonData['maxPage'] != 0):
            for i in range(1, jsonData['maxPage'] + 1):
                pages_list.append(f'{actual_url}{page_suffix}{i}')

    return pages_list
