import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import pandas as pd

#검색값 입력
print("쿠팡에서 물건 검색, 10순위+가격")
search = input("검색 : ")

driver = webdriver.Chrome('C:\Chrome_Driver\chromedriver.exe')


driver.get('https://www.coupang.com/')

driver.find_element_by_name('q').send_keys(search) #노트북이 검색값으로
driver.find_element_by_xpath('//*[@id="headerSearchBtn"]').click()

html = driver.page_source # 현재페이지
soup = BeautifulSoup(html, 'html.parser')

title_list = soup.find_all('div','name')
price_list = soup.find_all('strong','price-value')
result = []
"""
for i in price_list:
    result.append([i.get_text()])
    print(i.get_text())
"""
for i in range(0,10):
    result.append([title_list[i].get_text(), price_list[i].get_text()])
    print(title_list[i].get_text())

    
    
    
data = pd.DataFrame(result, columns = ['title','price'])

data.to_csv('testtest.csv', encoding = 'cp949')

#data.columns = ['title', 'price']    
#data.head()