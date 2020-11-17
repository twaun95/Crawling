
# coding: utf-8

# In[1]:

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup


# In[10]:

def chosun(search):
    URL = "http://search.chosun.com/search/news.search?query={search}&pageno=0&orderby=&naviarraystr=&kind=&cont1=&cont2=&cont5=&categoryname=&categoryd2=&c_scope=news&sdate=&edate=&premium=".format(search=search)
    driver = webdriver.Chrome("./chromedriver")
    driver.get(URL)
    
    resultURL = chosunURL(driver)
    chosunLinks(resultURL,driver)
    
def chosunURL(driver):
    
    URL = driver.current_url
    html = requests.get(URL) 
    bs = BeautifulSoup(html.text,"html.parser")  
    chosun = bs.select(".search_news_box dl dt ")
    
    i = len(chosun)
    int(i)
    
    resultURLs = chosun[0].select_one("a").attrs.get("href")
    return resultURLs

def chosunLinks(resultURL,driver):
        driver.get(resultURL)
        title = driver.find_element_by_css_selector(".news_title_text #news_title_text_id").text
        print("- 제목 - \n",title)
        subtitle = driver.find_elements_by_css_selector("#news_body_id .news_subtitle")[0].text
        print("- 부제목 - \n",subtitle)
        content = news_content(driver)
        print("- 본문 - \n",content)

def news_content(driver):
    pars = len(driver.find_elements_by_css_selector("#news_body_id .par")[:])
    pars_test=[]
    for i in range(pars) : 
        pars_test.append(driver.find_elements_by_css_selector("#news_body_id .par")[i].text)
    return ",".join(pars_test)

#search = input("검색 : ")    
search = "갤럭시"
chosun(search)


# In[ ]:



