import csv

import requests
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
           }

base_url = 'https://www.stimma.com.ua/shop'

# HTML

def get_html(url):
    session = requests.Session()
    request = session.get(url, headers=headers)
    if request.status_code == 200:
        return request.text
    return None

# soup

def get_soup(html, parser):
    if html:
        soup = bs(html, parser)
        return soup
    else:
        return None



if __name__ == '__main__':
    print(get_html(base_url))