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
    lis_css = 'body > div > table > tbody > tr > td > table:nth-child(2) > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(5) > td > table:nth-child(2) > tbody > tr > td:nth-child(2) > a'
    lis = response.css(lis_css)

    if (lis == []):
        add_error('pages', lis_css, logs, file_path, actual_url)
    else:
        for i in range(1, len(lis)+1):
            pages_list.append(actual_url + f'?page={i}&sort=1a')

    return pages_list
