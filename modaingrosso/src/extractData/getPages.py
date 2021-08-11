import os
from ..modules.logs.addLog import add_error
import json

# pages_list: string[] (ex. https://example.com/page1


def get_pages(response, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.url
    # @pages
    pages_list = []
    lis_css = '.woocommerce-pagination > ul > li'
    lis = response.css(lis_css)

    if (lis == []):
        add_error('pages', lis_css, logs, file_path, actual_url)
    else:
        for i in range(1, len(lis)):
            pages_list.append(actual_url + f'page/{i}/')

    return pages_list
