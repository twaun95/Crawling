
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup


# In[63]:

def chosun(search):
    URL = "http://search.chosun.com/search/news.search?query={search}&pageno=0&orderby=&naviarraystr=&kind=&cont1=&cont2=&cont5=&categoryname=&categoryd2=&c_scope=news&sdate=&edate=&premium=".format(search=search)
    driver = webdriver.Chrome("C:\Chrome_Driver\chromedriver.exe")
    driver.get(URL)
    
    return chosunURL(driver)

def chosunURL(driver):
    
    URL = driver.current_url
    html = requests.get(URL) 
    bs = BeautifulSoup(html.text,"html.parser")  
    chosun = bs.select(".search_news_box dl dt ")
    
    i = len(chosun)
    int(i)
    
    resultURLs = chosun[0].select_one("a").attrs.get("href")
    return print(resultURLs)


search = input("검색 : ")
#search = "강경화"
chosun(search)



