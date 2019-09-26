from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import time

npos_url = 'http://xxxxxxx/sitdealerdesktop/#!/login'
user_name = 'xxx'
pwd = 'xx!'
pin = 'xxx'

browser = webdriver.Chrome()
browser.get(npos_url)
browser.implicitly_wait(30)


def login():
    user = browser.find_element_by_xpath('//input[@placeholder="用户名"]')
    user.send_keys(user_name)
    password = browser.find_element_by_xpath('//input[@placeholder="密码"]')
    password.send_keys(pwd)
    pin_number = browser.find_element_by_xpath('//input[@placeholder="PIN码"]')
    pin_number.send_keys(pin)
    time.sleep(5)
    btn_login = browser.find_element_by_xpath('//*[@id="parallax-window"]/div/div/div[2]/div/button')
    btn_login.click()
    time.sleep(10)


def end_testing():
    browser.quit()


def create_quotation():
    btn_quotation = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div[1]/ul/li[1]/a')
    btn_quotation.click()
    time.sleep(3)
    # customer_name = browser.find_element_by_xpath('//input[@placeholder="名称"]')
    # customer_name.send_keys('金融报价单')
    # phone_number = browser.find_element_by_xpath('//input[@placeholder="手机号码"]')
    # phone_number.send_keys('13800138000')
    # btn_save = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/div[2]/ul/li[1]/a')
    # btn_save.click()
    # time.sleep(3)
    # btn_ok = browser.find_element_by_link_text('确定')
    # btn_ok.click()
    # btn_workQ = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/div[2]/ul/li[2]/a')
    # btn_workQ.click()
    # time.sleep(10)
    # btn_quotation.click()
    browser.find_element_by_xpath('//*[@id="anchor-quotation"]/div/div/div[2]/div[1]/div[1]/div[2]').click()
    time.sleep(3)
    browser.find_element_by_link_text('确定').click()
    # condition = browser.find_element_by_xpath('//input[@placeholder="车辆状况"]')
    elements = browser.find_elements_by_class_name('flex-1')
    select = Select(elements[1])
    select.select_by_visible_text("星时享")
    time.sleep(10)

    # customer_name.send_keys('租赁报价单')
    # phone_number.send_keys('13888888888')
    # btn_save.click()
    # time.sleep(3)
    # btn_ok = browser.find_element_by_link_text('确定')


if __name__ == '__main__':
    login()
    create_quotation()
    # end_testing()
