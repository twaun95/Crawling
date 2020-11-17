
# coding: utf-8

# In[1]:

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup


# In[4]:

resultURLs = []
def chosun(search):
    URL = "http://search.chosun.com/search/news.search?query={search}&pageno=0&orderby=&naviarraystr=&kind=&cont1=&cont2=&cont5=&categoryname=&categoryd2=&c_scope=news&sdate=&edate=&premium=".format(search=search)
    driver = webdriver.Chrome("./chromedriver")
    driver.get(URL)
    
    resultURLs = chosunURL(driver)
    chosunLinks(resultURLs,driver)
    
def chosunURL(driver):
    
    URL = driver.current_url
    html = requests.get(URL) 
    bs = BeautifulSoup(html.text,"html.parser")  
    chosun = bs.select(".search_news_box dl dt ")
    
    i = len(chosun)
    int(i)
    
    for name in chosun[0:i] :
        resultURLs.append(name.select_one("a").attrs.get("href"))
        
    return resultURLs

def chosunLinks(resultURLs,driver):
    chosuns_result = [
        [
            driver.get(content),
            driver.find_element_by_css_selector(".news_title_text #news_title_text_id").text,
            driver.find_elements_by_css_selector("#news_body_id .news_subtitle")[0].text,
            news_content(driver)
        ]
        for content
        in resultURLs
    ]

    for i in range(len(chosuns_result)):
        del chosuns_result[i][0]

    return print(chosuns_result)

def news_content(driver):
    pars = len(driver.find_elements_by_css_selector("#news_body_id .par")[:])
    pars_test=[]
    for i in range(pars) : 
        pars_test.append(driver.find_elements_by_css_selector("#news_body_id .par")[i].text)
    return ",".join(pars_test)

#search = input("검색 : ")    
search = "갤럭시"
chosun(search)

