from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests


options = webdriver.ChromeOptions()
# options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)
driver.get('https://www.mp3juices.cc/')
song_name = '夜的第7章'
driver.find_element_by_xpath('//*[@id="query"]').send_keys(song_name)
driver.find_element_by_xpath('//*[@id="button"]').click()

try:
    WebDriverWait(driver, 15, 1).until(ec.presence_of_element_located((By.ID, 'result_1')))
    driver.find_elements_by_link_text('Download')[0].click()
    WebDriverWait(driver, 15, 1).until(ec.presence_of_element_located((By.LINK_TEXT, 'Save to cloud')))
except Exception as ex:
    print('song not found.\n' + ex)
    driver.quit()
    exit(-1)

html = driver.execute_script("return document.documentElement.outerHTML")  # 获取点击后的页面 html 源码
bs = BeautifulSoup(html, 'html.parser')
download_1 = bs.find('div', {'id': 'download_1'})
mp3_url = download_1.find_all('a')[0]['href']

try:
    r = requests.get(mp3_url)
    save_path = 'C:/Users/eric.xu/Downloads/mp3/'
    print('Downloading...')
    with open(save_path + song_name + '.mp3', "wb") as f:
        f.write(r.content)
except Exception as ex:
    print(ex)

driver.quit()
