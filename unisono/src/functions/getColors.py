import os
from ..modules.logs.addLog import add_error

# colors_links_list: string[] (ex. https://example.com/color1)


def get_colors(self, response, logs, website):
    file_path = os.path.abspath(
        __file__)[os.path.abspath(__file__).find('src'):]
    actual_url = response.request.url

    # @colors_links
    colors_links_list = []
    colors_links_css = '.other-color a'
    colors_link_css = '::attr(href)'
    colors_links = response.css(colors_links_css)
    if (colors_links == []):
        colors_links_list.append(actual_url)
    else:
        for colorsLink in colors_links:
            # @colorsLink
            url = colorsLink.css(colors_link_css).get()
            if (url == None):
                add_error('colorsLink', colors_link_css,
                         logs, file_path, actual_url)
            else:
                colors_links_list.append(website + url)

    return(colors_links_list)
