import urllib.request
import regex
from bs4 import BeautifulSoup
import urllib
import re

def get_list(url, t):
    soup = get_soup(url)
    tag_text = t
    headers = soup.find('div', 'search-result').find_all('h2')
    for header in headers:
        if tag_text in header.text:
            tag = header
            break

    film_url = tag.findNext('ul').find_all('li')
    dict_url_and_movie = dict()
    for i in film_url:
        href = i.div.a.get('href')
        text = i.div.a.text
        dict_url_and_movie[text] = href
    return dict_url_and_movie

def get_soup(url):
    url = re.sub('\s', '+', url)

    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    request = urllib.request.Request(url, headers=headers)
    html_doc = urllib.request.urlopen(request).read()
    html_doc = html_doc.decode("utf-8")
    soup = BeautifulSoup(html_doc, 'html.parser')

    return soup
