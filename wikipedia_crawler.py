__author__ = 'Tanner_Hoke'

'''
wikipedia_crawler.py

This program can be run as a module or will run on its own.
Its purpose is to see if it is possible to find a specific
Wikipedia article from another. It does not use any AI methods
to determine the likelihood of different paths leading to the
end article, although I may add that at some point in the future.
The find_article function returns a boolean indicating whether the
article was found, and if it was the path variable passed will be
filled with what links the user needs to click in order to arrive
at the destination.

External modules:
BeautifulSoup
'''

import requests
from bs4 import BeautifulSoup
import webbrowser


def find_article(current_url, finish_url, max_depth, depth, path=[]):
    if 'Main_Page' in current_url:  # we really do not want to go to every link on the main page
        return False
    if current_url == finish_url:  # if we found it
        return True
    elif depth > max_depth:  # stop if we reached max depth
        return False

    start_source = requests.get(current_url)
    start_text = start_source.text
    start_soup = BeautifulSoup(start_text)

    for link in start_soup.findAll('a'):
        href = str(link.get('href'))
        if ':' in href or 'None' in href or href[0] == '/' and href[1] == '/':  # we don't want weird characters because
            continue                                                            # they don't lead to actual articles
        link_url = 'http://en.wikipedia.org' + href
        if '#' in link_url:
            continue
        if find_article(link_url, finish_url, max_depth, depth + 1, path):
            path.insert(0, link_url)  # insert into path so that the user knows how to get to the article
            return True


if __name__ == '__main__':
    print('Welcome to the Wikipedia crawler! It will tell you ' +
          'if it is possible to get from one article to another solely by clicking links.')
    url = input('URL to begin at:')
    end_url = input('URL to find:')
    path_holder = []
    deep = int(input('How deep to search (if you\'re not sure, use 1):'))
    if find_article(url, end_url, deep, 0, path_holder):
        print('Article found! Took', len(path_holder), 'clicks.')
        print('Opening path in browser...')
        for path_url in path_holder:
            print(path_url)
            webbrowser.open_new_tab(path_url)
    else:
        print('Could not find article.')