from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def yonhapnewsUrl(search):
    url = "http://www.yonhapnews.co.kr/home09/7091000000.html?query={search}&ctype=A".format(search=search)
    driver = webdriver.Chrome("./chromedriver.exe")
    driver.get(url)
    time.sleep(2)

    yonhapnewsUrlList(driver)

def yonhapnewsUrlList(driver):
    yonhapnewsUrs= driver.find_elements_by_css_selector(".cts_atclst li a")
    yonhapnewsUrs_List = []
    for urlList in yonhapnewsUrs:
        yonhapnewsUrs_List.append(urlList.get_attribute("href"))
        
    yonhapnewsInfo(driver,yonhapnewsUrs_List)

def yonhapnewsInfo(driver,yonhapnewsUrs_List):
    for urlList in yonhapnewsUrs_List:
        driver.get(urlList)
        time.sleep(2)
        newsTitle = driver.find_element_by_css_selector(".tit-article").text
        newsSubtitle = driver.find_element_by_css_selector(".stit strong").text
        # 기자
        newsTime = driver.find_element_by_css_selector(".share-info .tt em").text
        newsTime = newsTime[0:10].replace("/","")
        newsContents = driver.find_elements_by_css_selector(".article p")
        print("- 기사 제목 - : \n",newsTitle)
        print("- 기사 부제목 - \n:",newsSubtitle)
#        print("- 기사 송고시간 - \n:",newsTime)
        
        print("- 기사 본문 - \n")
        for content in newsContents:
            print(content.text,end=" ")

#search = input("검색 : ")

search = "인공지능"
yonhapnewsUrl(search)


# In[ ]:



