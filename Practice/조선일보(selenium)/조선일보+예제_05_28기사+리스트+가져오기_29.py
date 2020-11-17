
# coding: utf-8

# In[1]:

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup


# In[2]:

def chosun(search):
    URL = "http://search.chosun.com/search/news.search?query={search}&pageno=0&orderby=&naviarraystr=&kind=&cont1=&cont2=&cont5=&categoryname=&categoryd2=&c_scope=news&sdate=&edate=&premium=".format(search=search)
    driver = webdriver.Chrome("./chromedriver")
    driver.get(URL)
    
    chosunURL(driver)

def chosunURL(driver):
    
    URL = driver.current_url
    html = requests.get(URL) 
    bs = BeautifulSoup(html.text,"html.parser")  
    chosun = bs.select(".search_news_box dl dt ")
    
    i = len(chosun)
    int(i)
    
    print(" - 기사 리스트 URL - \n")
    for name in chosun[0:i] :
        print(name.select_one("a").attrs.get("href"))

#search = input("검색 : ")    
search = "삼다수"
chosun(search)


# In[ ]:



