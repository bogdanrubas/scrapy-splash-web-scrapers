import os
import json

# pages_list: string[] (ex. https://example.com/page1


def get_pages(response, logs, pagination_exists):
    actual_url = response.url

    # @pages
    pages_list = []
    lis_css = '.paginate-content > li'
    affix = '?page='

    lis = response.css(lis_css)

    if pagination_exists:
        for i in range(1, len(lis) - 1):
            pages_list.append(actual_url + f'{affix}{i}')
    else:
      pages_list.append(response.url)

    return pages_list
