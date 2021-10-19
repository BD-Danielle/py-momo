# -*- coding:utf-8 -*-

import os.path
import random
import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import pandas as pd
import urllib
from webdriver_manager.chrome import ChromeDriverManager

# from setuptools import setup, find_packages
# referer列表

momoUrl = 'https://www.momoshop.com.tw/main/Main.jsp'

# user_agent列表
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
headers = {'User-Agent': user_agent,
          'Referer': 'https://www.momoshop.com.tw'}

PATH = './chromedriver'
# driver = webdriver.Chrome(PATH)
driver = webdriver.Chrome(ChromeDriverManager().install())

dict = {"prdName": [], "price": [], "goodsUrl": [], "prdImg": []}

def url(keyword, pageNo):
  url = 'https://www.momoshop.com.tw/search/searchShop.jsp?keyword={}&searchType=6&curPage={}&_isFuzzy=0&showType=chessboardType'.format(keyword, pageNo)
  print(url)
  return url

# 打開瀏灠器模擬器
def open_chrome_browser(keyword, pageNo):
  driver.get(url(keyword, pageNo))
  driver.implicitly_wait(10)
#   search = driver.find_element_by_name('keyword')
#   search.send_keys('即期品')
#   search.send_keys(Keys.RETURN)
  time.sleep(random.randrange(10))
  driver.implicitly_wait(30)

def mimic_human():
  try:
    html = driver.find_element_by_tag_name('html')
    # 模擬人為操作頁面
    for x in range(6):
      html.send_keys(Keys.END)
      time.sleep(random.randrange(10))
      html.send_keys(Keys.END)
      time.sleep(random.randrange(10))
    print("Finally finished!")
  except TimeoutException:
    print("Timed out waiting for page to load")
  finally:
    print("Page loaded")

def get_last_pageNo():
  lastPage = driver.find_element_by_css_selector('.pageArea > ul > li:last-child > a')
  lastPageNo = int(lastPage.get_attribute('pageidx'), base = 10)
  print(lastPageNo)
  return lastPageNo

def give_a_break(n):
    time.sleep(random.randrange(n))

def download_page(element, n):
  if (element.is_displayed()):
    with open('momo{}.html'.format(n), 'w') as f:
      f.write(driver.page_source)
  else:
    print('element display none')

def exit():
  driver.quit()

def dfToExcel(dict):
  df = pd.DataFrame(dict)
  df[['prdName', 'price', 'goodsUrl', 'prdImg']].to_excel('output.xlsx')

def write_to_dict(n):
  if(os.path.exists('momo{}.html'.format(n))):
    with open('momo{}.html'.format(n), 'r') as f:
      contents = f.read()
      soup = BeautifulSoup(contents, 'html.parser')
      goods = soup.select('.listArea > ul > li')
    for good in goods:
      dict["prdName"].append(good.select('.prdName')[0].text)
      dict["price"].append(good.select('.price > b')[0].text)
      dict["goodsUrl"].append('https://www.momoshop.com.tw/' + good.select('.goodsUrl')[0]['href'])
      dict["prdImg"].append(good.select('.prdImg')[0]['src'])
  else:
    print('file not exists')

if __name__ == '__main__':
  open_chrome_browser('澳洲', 1)
  n = get_last_pageNo()
  i = 1
  while i <= n:
    open_chrome_browser('澳洲', i)
    mimic_human()
    element = driver.find_element_by_css_selector('.listArea > ul > li')
    print('next page')
    download_page(element, i)
    write_to_dict(i)
    i+=1
dfToExcel(dict)
print('finally finished')
exit()
