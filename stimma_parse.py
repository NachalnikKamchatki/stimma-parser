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

# getting count of pages

def get_pages(soup):
    urls = []
    if soup:
        nav_links = soup.find('div', class_="nav-links")
        pages_count = int(nav_links.find_all('a')[-2].text)
    return pages_count

# parsing data


def parse(soup):
    products = []
    if soup:
        divs = soup.find_all('div', class_="product-h")

        for div in divs:
            try:
                title = div.find('h2', class_="woocommerce-loop-product__title").text
                href = div.find('a')['href']
                img_link = div.find('img', class_="attachment-woocommerce_thumbnail size-woocommerce_thumbnail")['src']
                price = div.find('span', class_="price").text
                products.append(
                    {
                        'title': title.strip(),
                        'href': href.strip(),
                        'image_link': img_link.strip(),
                        'price': price.strip(),
                    }

                )

            except:
                pass
        return products
    else:
        print('ERROR!!! ERROR!!!')

# recording data to csv_file


def files_writer(results, filename):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(('Название вакансии', 'URL', 'Название компании', 'Цена'))
        for result in results:
            writer.writerow((result['title'], result['href'], result['image_link'], result['price'],))


if __name__ == '__main__':
    results = []
    html = get_html(base_url)
    soup = get_soup(html, 'lxml')
    count_pages = get_pages(soup)
    for i in range(1, count_pages):
        print('Page ' + str(i))
        html = get_html(base_url + '/page/' + str(i))
        soup = get_soup(html, 'lxml')
        products = parse(soup)
        try:
            results.extend(products)
        except:
            print('passed')
            pass

    files_writer(results, 'parsed_products.csv')



