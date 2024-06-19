from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
import lxml
from time import sleep
import username_password

with open('proxies.txt', 'r') as f:
    proxies_text = f.read()
    proxy_list = proxies_text.split('\n')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

url = 'https://www.fragrantica.com/awards2023/category/Best-Men-s-Perfume-of-All-Time'

top_notes = []
mid_notes = []
base_notes = []

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url)
    page.wait_for_timeout(3000)
    page_content = page.content()

    soup = BeautifulSoup(page_content, 'lxml')
    divs = soup.find_all('div', class_='flex-dir-column')[:100]
    url_list = []

    for div in divs:
        a_tag = div.find('a')
        url = 'https://www.fragrantica.com' + a_tag['href']
        url_list.append(url)

    for i, url in enumerate(url_list):
        if i == 70:
            sleep(900)
            print('waiting for 15 minutes')

        top_this = []
        mid_this = []
        base_this = []

        proxy = {
            'http': f'http://{username_password.username}:{username_password.password}@{proxy_list[i%len(proxy_list)]}',
            'https': f'http://{username_password.username}:{username_password.password}@{proxy_list[i%len(proxy_list)]}'
        }

        # http:// username : password @ ipnumber : portnumber

        sleep(3)

        response = requests.get(url, headers=headers, proxies=proxy)

        html_text = response.text
        soup = BeautifulSoup(html_text, 'lxml')

        if soup.find('b', string='Top Notes') is not None:
            top_pyramid = soup.find('pyramid-level', attrs={"notes": "top"})
            a_tags = top_pyramid.find_all('a')

            for a_tag in a_tags:
                parent_element = a_tag.parent
                top_this.append(parent_element.text.strip())

            mid_pyramid = soup.find('pyramid-level', attrs={"notes": "middle"})
            a_tags = mid_pyramid.find_all('a')

            for a_tag in a_tags:
                parent_element = a_tag.parent
                mid_this.append(parent_element.text.strip())

            base_pyramid = soup.find('pyramid-level', attrs={"notes": "base"})
            a_tags = base_pyramid.find_all('a')

            for a_tag in a_tags:
                parent_element = a_tag.parent
                base_this.append(parent_element.text.strip())

        else:
            only_pyramid = soup.find('pyramid-level', attrs={"notes": "ingredients"})
            a_tags = only_pyramid.find_all('a')
            for a_tag in a_tags:
                parent_element = a_tag.parent
                top_this.append(parent_element.text.strip())
                mid_this.append(parent_element.text.strip())
                base_this.append(parent_element.text.strip())

        top_notes.extend(top_this)
        mid_notes.extend(mid_this)
        base_notes.extend(base_this)

with open('top.txt', 'w') as f:
    for note in top_notes:
        f.write(f'{note}\n')

with open('mid.txt', 'w') as f:
    for note in mid_notes:
        f.write(f'{note}\n')

with open('base.txt', 'w') as f:
    for note in base_notes:
        f.write(f'{note}\n')