
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



def chosun(search):
    URL = "http://search.chosun.com/search/news.search?query={search}&pageno=0&orderby=&naviarraystr=&kind=&cont1=&cont2=&cont5=&categoryname=&categoryd2=&c_scope=news&sdate=&edate=&premium=".format(search=search)
    driver = webdriver.Chrome("C:\Chrome_Driver\chromedriver.exe")
    driver.get(URL)
    
#    chosun_search = driver.find_elements_by_css_selector("#menuGnb li")
#    print(chosun_search)
#    chosun_search[1].click()

#    chosun_search2 = driver.find_elements_by_css_selector("#opt_source dd a")
#    chosun_search2[0].click()

#search = input("검색 : ")    
search = "갤럭시"
chosun(search)




