import os
from ..modules.logs.addLog import add_error

# pages_list: string[] (ex. https://example.com/page1)


def get_pages(self, response, logs, website):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.meta.get('actual_url')

    # @pages
    pages_list = []
    pages_css = '.pagination > li'
    page_css = 'a::attr(href)'
    last_page_css = '.pagination > li:last-of-type > a::attr(href)'
    pages = response.css(pages_css)
    if (pages == []):
        add_error('pages', pages_css, logs, file_path, actual_url)
    else:
        pages_list.append(actual_url)
        if (len(pages) > 2):
            for page in pages:
                index = pages.index(page)
                if (index < len(pages) - 1 and index > 0):
                    url = page.css(page_css).get()
                    pages_list.append(website + url)
        elif (len(pages) == 2):
            last_page_url = response.css(last_page_css).get()
            pages_list.append(website + last_page_url)

    return(pages_list)
