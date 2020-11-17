from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymysql
import time

def 매일경제(search):
    url = "http://find.mk.co.kr/new/search.php"
    driver = webdriver.Chrome("../chromedriver.exe")
    driver.get(url)
    time.sleep(2)

    inputNews = driver.find_element_by_id("search")
    inputNews.send_keys(search)
    inputNews.send_keys(Keys.ENTER)

    moreInfo = driver.find_elements_by_css_selector("tbody tr .class_more a")  
    infoJss = []
    infoJss.append(moreInfo[0].get_attribute("href"))
    moreBtn =moreInfo[0].get_attribute("href")
    driver.execute_script(moreBtn)
    
    mkUrlList(driver)

def mkUrlList(driver):
    url2 = driver.current_url
    yonhapnewsUrs_List = []
    for pageNo in range(1,6): #2페이지까지
        url = url2 + "&pageNum={pageNo}".format(pageNo=pageNo)
        driver.get(url)
        yonhapnewsUrs= driver.find_elements_by_css_selector("table tbody tr td .sub_list .art_tit a")
    
        for urlList in yonhapnewsUrs:
            yonhapnewsUrs_List.append(urlList.get_attribute("href"))

        mkInfo(driver,yonhapnewsUrs_List)

def mkInfo(driver,yonhapnewsUrs_List):
    for urlList in yonhapnewsUrs_List:
        driver.get(urlList)
        
        if driver.find_elements_by_css_selector(".news_title_author .lasttime") != [] :
            newsDate = driver.find_element_by_css_selector(".news_title_author .lasttime").text.replace("입력 : ","").replace(".","")[0:8]
        else :
            newsDate = driver.find_element_by_css_selector(".news_title_author .lasttime1").text.replace("입력 : ","").replace(".","")[0:8]
        
        newsTitle = driver.find_element_by_css_selector(".top_title").text
        newsSubtitles = driver.find_elements_by_css_selector("#article_body")
        newsSubtitle_result = ""
        for newsSubtitle in newsSubtitles:
            newsSubtitle_result+=newsSubtitle.text
        content_result = driver.find_element_by_css_selector(".art_txt").text
            
        print("- url - : \n",urlList)
        print("- 날짜 - : \n",newsDate)        
        print("- 기사 제목 - : \n",newsTitle)
#        print("- 기사 부제목 - \n:",newsSubtitle_result)
#        print("- 기사 본문 - \n")
#        print(content_result)

        dbData = [[urlList,newsDate,newsTitle,newsSubtitle_result,content_result]]
        connectDB(dbData)
        
def connectDB(dbData):
    DB_HOST = '127.0.0.1'
    DB_USER = 'root'
    DB_PASSWD = 'autoset'
    DB_NAME = 'python'
    
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWD,
                       db=DB_NAME, charset='utf8')
    
    curs = conn.cursor()

    sql = """insert into news(url,newsDate, newsTitle,newsSubtitle,content)
         values (%s, %s, %s, %s, %s)"""
    curs.executemany(sql,dbData)
    
    conn.commit()

    conn.close()
    
#search = input("검색 : ")
search = "인공지능"
매일경제(search)

