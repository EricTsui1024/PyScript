# coding : UTF-8
import random
import requests
import os
from bs4 import BeautifulSoup

home_URL = 'https://xkcd.com/'

request_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5478.400 QQBrowser/10.1.1550.400'
}


def get_total_pages():
    try:
        r = requests.get(home_URL, headers=request_headers)
        r.encoding = 'UTF-8'
        bs = BeautifulSoup(r.text, "html.parser")
        prev = bs.find('ul', {'class': 'comicNav'}).find_all('li')[1].a['href']
        prev = prev.replace('/', '')
        return int(prev) + 1

    except Exception as e:
        print(e)
        return 1


def save_pic(page_num):
    timeout = random.choice(range(60, 180))
    try:
        r = requests.get(home_URL+str(page_num), headers=request_headers, timeout=timeout)
        r.encoding = 'UTF-8'
        bs = BeautifulSoup(r.text, "html.parser")
        img = bs.find('div', {'id': 'comic'}).find('img')
        pic_url = ' https:' + img['src']
        img_name = path + os.path.basename(pic_url)

        r = requests.get(pic_url)
        with open(img_name, 'wb') as file:
            file.write(r.content)

        print('Downloading page number: ' + str(page_num) + pic_url)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    total_pages = get_total_pages()
    path = os.getcwd() + '/xkcd/'
    if not os.path.exists(path):
        os.makedirs(path)

    for i in range(1, total_pages + 1):
        save_pic(i)
