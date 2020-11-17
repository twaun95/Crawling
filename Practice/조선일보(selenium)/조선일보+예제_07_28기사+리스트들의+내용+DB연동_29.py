import pymysql
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import requests
from bs4 import BeautifulSoup



resultURLs = []
chosuns_result = []

def news_content(driver):
    pars = len(driver.find_elements_by_css_selector("#news_body_id .par")[:])
    pars_test=[]
    for i in range(pars) : 
        pars_test.append(driver.find_elements_by_css_selector("#news_body_id .par")[i].text)
    return ",".join(pars_test)

def chosunURL(driver):
    
    URL = driver.current_url
    html = requests.get(URL) 
    bs = BeautifulSoup(html.text,"html.parser")  
    chosun = bs.select(".result.news dl dt ")
    
    i = len(chosun)
    int(i)
    
    for name in chosun[0:i] :
        resultURLs.append(name.select_one("a").attrs.get("href"))
    
    return resultURLs

def chosunLinks(resultURLs,driver):
    for content in resultURLs:
        driver.get(content)
        a = driver.find_element_by_css_selector(".news_title_text #news_title_text_id").text
        b = driver.find_elements_by_css_selector("#news_body_id .news_subtitle")[0].text
        c = news_content(driver)
        d = [[a,b,c]]
        connectDB(d)

def connectDB(d):
    DB_HOST = '127.0.0.1'
    DB_USER = 'root'
    DB_PASSWD = 'autoset'
    DB_NAME = 'python'
    
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWD,
                       db=DB_NAME, charset='utf8')
    
    curs = conn.cursor()

    sql = """insert into pythonTest(title,subject,content)
         values (%s, %s, %s)"""
    curs.executemany(sql,d)
    conn.commit()

    conn.close()
    
def chosun(search):
    URL = "http://search.chosun.com/search/total.search?query={search}&pageconf=total".format(search=search)
    driver = webdriver.Chrome("./chromedriver")
    driver.get(URL)
    

    chosun_search = driver.find_elements_by_css_selector(".main_menu li")
    chosun_search[1].click()

    chosun_search2 = driver.find_elements_by_css_selector("#opt_source dd a")
    chosun_search2[0].click()
    
    resultURLs = chosunURL(driver)
    chosunLinks(resultURLs,driver)


search = input("검색 : ")
chosun(search)

