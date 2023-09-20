# selenium-crawler-momo
============================================

### 用關鍵字遍歷[MOMO](https://www.momoshop.com.tw/main/Main.jsp)購物網站，將搜尋結果清單存入excel
### Using keywords to traverse momo shopping sites and save the search result list to excel

1. 專門針對[MOMO](https://www.momoshop.com.tw/main/Main.jsp)購物網站的產品品項，去做遍歷並存取其產品資訊，以供數據分析。
2. 無需登入個人資訊。
3. 彈出廣告不影響搜尋結果。

快速入門
=======
```
pip install -e git+https://github.com/shutuzi88/selenium-crawler.git#egg=selenium-crawler

```
```python
if __name__ == '__main__':
  open_chrome_browser('keyword', 1)
  n = get_last_pageNo()
  i = 1
  while i <= n:
    open_chrome_browser('keyword', i)
    mimic_human()
    element = driver.find_element_by_css_selector('.listArea > ul > li')
    print('next page')
    download_page(element, i)
    write_to_dict(i)
    i+=1
dfToExcel(dict)
exit()
```
