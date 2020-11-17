import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import pandas as pd


print("1번: 3-Months / 2번: 12-Months / 3번: Year to Date")
search = int(input("번호 선택 : "))

 
driver = webdriver.Chrome('C:\Chrome_Driver\chromedriver.exe')
if search == 1:

    driver.get('https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20190227&end=20190527')

elif search == 2:

    driver.get('https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20180527&end=20190527')

elif search == 3:

    driver.get('https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20190101&end=20190527')


html = driver.page_source # 현재페이지
soup = BeautifulSoup(html, 'html.parser')

table = soup.find('table', {'class': 'table'})

result = []

for tr in table.find_all('tr','text-right'):

    tds = list(tr.find_all('td'))

    date = tds[0].text

    opent = tds[1].text

    high = tds[2].text

    low = tds[3].text

    close = tds[4].text

    volume = tds[5].text

    cap = tds[6].text

    result.append([date, opent, high, low, close, volume, cap])


#result

data = pd.DataFrame(result, columns=['Data', 'Open', 'High', 'Low', 'Close', 'Volume', 'Cap'])
data.to_csv('bitcoin.csv', encoding = 'cp949')
