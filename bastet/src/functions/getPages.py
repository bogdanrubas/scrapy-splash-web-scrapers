import os
import json

# pages_list: string[] (ex. https://example.com/page1


def get_pages(response, logs):
    actual_url = response.url

    # @pages
    pages_list = []
    list_css = 'ul.page-numbers > li'

    lis = response.css(list_css)

    if (lis == []):
        pages_list.append(actual_url)
    else:

        for i in range(0, len(lis)):
            if i == len(lis) - 2:
                last_page = lis[i].css('a::text').get()
                for i in range(1, int(last_page) + 1):
                    pages_list.append(actual_url + f'page/{i}/')

    return pages_list
