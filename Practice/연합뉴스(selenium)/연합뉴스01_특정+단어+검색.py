from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def yonhapnewsUrl(search):
    url = "http://www.yonhapnews.co.kr/home09/7091000000.html?query={search}&ctype=A".format(search=search)
    driver = webdriver.Chrome("./chromedriver.exe")
    driver.get(url)
    
#search = input("검색 : ")
search = "수리온"
yonhapnewsUrl(search)

