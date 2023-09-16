# -*- coding:utf-8 -*-
import os
import time
import random
import urllib.parse
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Momo URL
MOMO_URL = 'https://www.momoshop.com.tw/main/Main.jsp'

# User agent
USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36')
HEADERS = {'User-Agent': USER_AGENT, 'Referer': 'https://www.momoshop.com.tw'}

# Set up the Chrome driver
driver = webdriver.Chrome()


def generate_url(keyword, page_no):
    return f'https://www.momoshop.com.tw/search/searchShop.jsp?keyword={urllib.parse.quote(keyword)}&searchType=6&curPage={page_no}&_isFuzzy=0&showType=chessboardType'


def open_chrome_browser(keyword, page_no):
    url = generate_url(keyword, page_no)
    driver.get(url)
    driver.implicitly_wait(10)
    time.sleep(random.randrange(10))
    driver.implicitly_wait(30)


def mimic_human():
    try:
        html = driver.find_element(By.TAG_NAME, 'html')
        # Simulate human interaction with the page
        for _ in range(6):
            html.send_keys(Keys.END)
            time.sleep(random.randrange(10))
            html.send_keys(Keys.END)
            time.sleep(random.randrange(10))
        print("Finally finished!")
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        print("Page loaded")


def get_last_page_no():
    last_page = driver.find_element(By.CSS_SELECTOR, '.pageArea > ul > li:last-child > a')
    last_page_no = int(last_page.get_attribute('pageidx'))
    print(last_page_no)
    return last_page_no


def give_a_break(n):
    time.sleep(random.randrange(n))


def download_page(element, n):
    if element.is_displayed():
        with open(f'momo{n}.html', 'w') as f:
            f.write(driver.page_source)
    else:
        print('element display none')


def df_to_excel(data_dict):
    df = pd.DataFrame(data_dict)
    df[['prdName', 'price', 'goodsUrl', 'prdImg']].to_excel('output.xlsx')


def write_to_dict(n, data_dict):
    file_path = f'momo{n}.html'
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            contents = f.read()
            soup = BeautifulSoup(contents, 'html.parser')
            goods = soup.select('.listArea > ul > li')
            for good in goods:
                data_dict["prdName"].append(good.select_one('.prdName').text)
                data_dict["price"].append(good.select_one('.price > b').text)
                data_dict["goodsUrl"].append('https://www.momoshop.com.tw/' + good.select_one('.goodsUrl')['href'])
                data_dict["prdImg"].append(good.select_one('.prdImg')['src'])
    else:
        print('File not exists')


if __name__ == '__main__':
    keyword = '即期品'
    open_chrome_browser(keyword, 1)
    last_page_no = get_last_page_no()
    data_dict = {"prdName": [], "price": [], "goodsUrl": [], "prdImg": []}

    for i in range(1, last_page_no + 1):
        open_chrome_browser(keyword, i)
        mimic_human()
        element = driver.find_element(By.CSS_SELECTOR, '.listArea > ul > li')
        print('Next page')
        download_page(element, i)
        write_to_dict(i, data_dict)
        # give_a_break(random.randrange(10))

    df_to_excel(data_dict)
    print('Finally finished')
    driver.quit()
