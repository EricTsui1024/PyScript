# coding : UTF-8
import os
import requests
import csv
import random
import time
import datetime
from bs4 import BeautifulSoup

request_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/69.0.3497.100 Safari/537.36'
}

cookies = {}


# cookie 需要跟 header 的 UA 一致
def set_cookies(cookies_path):
    try:
        f = open(cookies_path, 'r')
        for line in f.read().split(';'):
            name, value = line.strip().split('=', 1)
            cookies[name] = value
    except Exception as e:
            print('set_cookies ERROR:', e)


def get_html(url):
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url, headers=request_headers, cookies=cookies, timeout=timeout)
            rep.encoding = 'UTF-8'
            break

        except Exception as e:
            print('get_html ERROR:', e)
            time.sleep(random.choice(range(5, 15)))

    return rep.text


def get_data(html_text):
    final = []
    bs = BeautifulSoup(html_text, "html.parser")
    li = bs.find('ul', {'class': 'carlist clearfix js-top'}).find_all('li')

    for car in li:
        try:
            temp = []
            a = car.find('a')
            msrp = a.find('em').string
            car_info = car.text.split('\n')
            car_name = car_info[3]
            price = car_info[8]
            three_info = car_info[5].split('|')
            car_year = ''
            mileage = ''
            city = ''
            try:
                car_year = three_info[0]
                mileage = three_info[1]
                city = three_info[2]
            except Exception as e:
                pass

            temp.append(city)
            temp.append(car_name)
            temp.append(car_year)
            temp.append(mileage)
            temp.append(price)
            temp.append(msrp)
            temp.append(today_date)
            # temp.append('瓜子网')

            final.append(temp)
        except Exception as e:
            print('get_data: ', e)
            continue

    return final


def save_data(data, name):
    file_name = name
    try:
        with open(file_name, 'a', errors='ignore', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(data)
    except Exception as e:
        print('save_data: ', e)


def get_all_pages(home_url):
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(home_url, headers=request_headers, cookies=cookies, timeout=timeout)
            rep.encoding = 'UTF-8'
            break

        except Exception as e:
            print('get_all_pages ERROR:', e)
            time.sleep(random.choice(range(5, 15)))

    bs = BeautifulSoup(rep.text, "html.parser")
    all_span = bs.find('div', {'class': 'pageBox'}).find_all('span')
    page_index = int(all_span[len(all_span) - 2].string)

    return page_index


if __name__ == '__main__':
    set_cookies(os.getcwd() + '/guazi_cookie.txt')
    # requests.packages.urllib3.disable_warnings()

    all_pages = get_all_pages('https://www.guazi.com/www/buy/')

    for page_num in range(1, all_pages):
        try:
            car_url = 'https://www.guazi.com/www/buy/o' + str(page_num)
            print(car_url)
            html = get_html(car_url)
            today_date = datetime.date.today()
            time.sleep(1)
            result = get_data(html)
            save_data(result, os.getcwd() + '/guazi_car.csv')
        except Exception as error:
            print(error)
            continue
