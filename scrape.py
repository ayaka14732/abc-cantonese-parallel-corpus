from bs4 import BeautifulSoup
import requests

cookies = {
    'wenlinco_wowdbUserName': ...,
    'wenlinco_wowdbUserID': ...,
    'wenlinco_wowdb_session': ...,
}

def write_titles(titles: list[str], filename: str='titles.txt') -> None:
    with open(filename, 'a', encoding='utf-8') as f:
        for title in titles:
            print(title, file=f)

def get_next_page_url(soup) -> str | None:
    navs = soup.select('.mw-allpages-nav > a')
    for nav in navs:
        if nav.get_text().startswith('Next page'):
            return nav['href']

def get_titles(soup) -> list[str]:
    links = soup.select('.mw-allpages-body li > a')
    titles = [link['title'] for link in links]
    return titles

base_url = 'https://wenlin.co'
session = requests.Session()
session.headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

i = 0
url = '/wow/Special:AllPages?from=&to=&namespace=3188&hideredirects=1'
while url is not None:
    response = requests.get(base_url + url, cookies=cookies)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = get_titles(soup)
    write_titles(titles)
    url = get_next_page_url(soup)
    i += 1
    print(f'Finished page {i}.')
