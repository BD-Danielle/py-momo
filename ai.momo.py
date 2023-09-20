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

# Constants
MOMO_URL = 'https://www.momoshop.com.tw/main/Main.jsp'
USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
)
HEADERS = {'User-Agent': USER_AGENT, 'Referer': 'https://www.momoshop.com.tw'}

# Global variables
driver = webdriver.Chrome()


def generate_search_url(keyword, page_no):
    return f'https://www.momoshop.com.tw/search/searchShop.jsp?keyword={urllib.parse.quote(keyword)}&searchType=6&curPage={page_no}&_isFuzzy=0&showType=chessboardType'


def open_chrome_browser(keyword, page_no):
    url = generate_search_url(keyword, page_no)
    driver.get(url)
    driver.implicitly_wait(random.randrange(10))
    time.sleep(random.randrange(10))
    driver.implicitly_wait(random.randrange(10))


def mimic_human_scroll():
    try:
        html = driver.find_element(By.TAG_NAME, 'html')
        for _ in range(6):
            html.send_keys(Keys.END)
            time.sleep(random.randrange(10))
            html.send_keys(Keys.END)
            time.sleep(random.randrange(10))
        print("Finally finished!")
    except TimeoutException:
        print("Timed out waiting for the page to load")
    finally:
        print("Page loaded")


def get_last_page_number():
    last_page_elem = driver.find_element(
        By.CSS_SELECTOR, '.pageArea > ul > li:last-child > a')
    last_page_no = int(last_page_elem.get_attribute('pageidx'))
    print(f'Last page number: {last_page_no}')
    return last_page_no


def wait_for_a_while(n):
    time.sleep(n)


def download_page_to_file(element, n, keyword_folder):
    if not os.path.exists(keyword_folder):
        os.makedirs(keyword_folder)

    if element.is_displayed():
        with open(os.path.join(keyword_folder, f'momo{n}.html'), 'w') as f:
            f.write(driver.page_source)
    else:
        print('Element is not displayed')


def df_to_excel(data_dict, keyword_folder):
    if not os.path.exists(keyword_folder):
        os.makedirs(keyword_folder)

    file_path = os.path.join(keyword_folder, 'output.xlsx')
    df = pd.DataFrame(data_dict)
    df[['prdName', 'price', 'goodsUrl', 'prdImg']].to_excel(file_path, index=False)


def parse_html_to_dict(n, data_dict, keyword_folder):
    file_path = os.path.join(keyword_folder, f'momo{n}.html')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            contents = f.read()
            soup = BeautifulSoup(contents, 'html.parser')
            goods = soup.select('.listArea > ul > li')
            for good in goods:
                data_dict["prdName"].append(good.select_one('.prdName').text)
                data_dict["price"].append(good.select_one('.price > b').text)
                data_dict["goodsUrl"].append(
                    'https://www.momoshop.com.tw/' + good.select_one('.goodsUrl')['href'])
                data_dict["prdImg"].append(good.select_one('.prdImg')['src'])
    else:
        print('File does not exist')


KEYWORD = '橄欖油'
if __name__ == '__main__':
    if not KEYWORD:
        KEYWORD = input("Please type the keyword: ")

    open_chrome_browser(KEYWORD, 1)
    last_page_no = get_last_page_number()
    data_dict = {"prdName": [], "price": [], "goodsUrl": [], "prdImg": []}
    # Replace spaces with underscores for the folder name
    keyword_folder = KEYWORD.replace(" ", "_")

    for i in range(1, last_page_no + 1):
        open_chrome_browser(KEYWORD, i)
        # mimic_human_scroll()
        element = driver.find_element(By.CSS_SELECTOR, '.listArea > ul > li')
        print('Next page')
        download_page_to_file(element, i, keyword_folder)
        parse_html_to_dict(i, data_dict, keyword_folder)
        wait_for_a_while(random.randrange(10))

    df_to_excel(data_dict, keyword_folder)
    print('Finally finished')
    driver.quit()
