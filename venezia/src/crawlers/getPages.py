import os
from ..modules.logs.addLog import add_error

# pages_list: string[] (ex. https://example.com/page1

def get_pages(self, response, pagination_exists, website, logs):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('scraper'):]
    actual_url = response.meta.get('actual_url')
    # @pages
    pages_list = []
    pages_css = '.pages_list > a'
    page_css = '::attr(href)'

    if pagination_exists == True:
        pages = response.css(pages_css)
        if (pages == []):
            add_error('pages', pages_css, logs, file_path, actual_url)
        elif(len(pages) == 1):
            pages_list.append(actual_url)
        else:
            for page in pages:
                # @url
                url = page.css(page_css).get()
                if (url == None):
                    add_error('page', page_css, logs, file_path, actual_url)
                else:
                    pages_list.append(website + url)
    else:
        pages_list.append(actual_url)
    return pages_list
