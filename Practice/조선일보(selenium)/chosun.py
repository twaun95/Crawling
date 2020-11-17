from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymysql
import time

# 1단계 사이트 기동
def chosun2015(search):
    url="http://search.chosun.com/search/news.search?query={search}&orderby=docdatetime&naviarraystr=&kind=&cont1=&cont2=&cont5=&categoryname=&categoryd2=&c_scope=&sdate=&edate=&premium=".format(search=search)
    driver = webdriver.Chrome("./chromedriver.exe")
    driver.get(url)
    time.sleep(2)
    
    조선UrlList(driver)

def 조선UrlList(driver):
    url2 = driver.current_url
    for pageNo in range(1,3): # 2015년: 175~265페이지(2017.10.25기준)
        url = url2 + "&pageno={pageNo}".format(pageNo=pageNo)
        driver.get(url)
        time.sleep(2)
        
        조선href =[]
        조선Urls= driver.find_elements_by_css_selector(".search_news_box .search_news .thumb a")
        for x in 조선Urls:
            if x.get_attribute("href")[7:11] == "news":
                조선href.append(x.get_attribute("href"))
            else:
                pass

#        for x in 조선Urs_List:
#            print("url은",x,"슬라이싱",x[7:11])

        조선Info(driver,조선href)

def 조선Info(driver,조선href):
    for urlList in 조선href:
        driver.get(urlList)
        time.sleep(2)
        try:

            newsDate = driver.find_element_by_css_selector(".date_ctrl_2011 #date_text").text.replace("입력 : ","").replace(".","").replace("\n","").replace("\r","").replace("\t","")[0:8]
            newsTitle = driver.find_element_by_css_selector(".news_title_text #news_title_text_id").text

            newsSubtitles = driver.find_elements_by_css_selector("#news_body_id .news_subtitle")
            newSubtitle = ""
            for newsSubtitles_x in newsSubtitles:
                newSubtitle += newsSubtitles_x.text

            newsContents = driver.find_elements_by_css_selector("#news_body_id .par")
            if newsContents != []:  # []대신 ""을 넣었더니 안됐는데, ""는 문자열이라서 element 단수를 받을 때 쓰고 []는 elements 복수-리스트를 받을 때 쓴다.
                newsContents = driver.find_elements_by_css_selector("#news_body_id .par")
                newsContent = ""
                for i in range(len(newsContents)) :
                    newsContent += newsContents[i].text
            else :
                newsContents = driver.find_elements_by_css_selector("#news_body_id p")
                newsContent = ""
                for i in range(len(newsContents)) :
                    newsContent += newsContents[i].text
 
            print("- url - : \n",urlList)
            print("- 날짜 - : \n",newsDate)        
            print("- 기사 제목 - : \n",newsTitle)
            print("- 기사 부제목 - \n:",newSubtitle)
            print("- 기사 본문 - \n",newsContent)
            
            dbData = [[urlList,newsDate,newsTitle,newSubtitle,newsContent]]
            connectDB(dbData)
        except :
            continue
        
def connectDB(dbData):
    DB_HOST = '127.0.0.1'
    DB_USER = 'root'
    DB_PASSWD = 'autoset'
    DB_NAME = 'python'
    
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWD,
                       db=DB_NAME, charset='utf8')
    
    curs = conn.cursor()

    sql = """insert into chosun(url,newsDate,newsTitle,newsSubtitle,content)
         values (%s, %s, %s, %s, %s)"""
    curs.executemany(sql,dbData)
    
    conn.commit()

    conn.close()

search="원자력"    
#search = input("검색 : ")
chosun2015(search)


