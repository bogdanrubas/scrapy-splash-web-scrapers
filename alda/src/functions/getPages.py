import os
import json

# pages_list: string[] (ex. https://example.com/page1

def get_pages(response, logs):
    filePath = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('scraper'):]
    actual_url = response.url

    # @pages
    pages_list = []
    lis_css = '.pagination ul li > a'
    page_suffix = '?page='

    lis = response.css(lis_css)

    if (lis == []):
        pages_list.append(actual_url)
    else:
        for i in range(0, len(lis) - 1):
            pages_list.append(f'{actual_url}{page_suffix}{i + 1}')

    return pages_list
