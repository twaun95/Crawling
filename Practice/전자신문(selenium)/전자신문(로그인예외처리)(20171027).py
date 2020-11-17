from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymysql
import time


def 전자신문(search):
    url = "http://search.etnews.com/etnews/search.php?category=CATEGORY1&kwd={search}&pageSize=10&reSrchFlag=false&sort=1&startDate=&endDate=&sitegubun=&jisikgubun=&preKwd%5B0%5D=4%EC%B0%A8%EC%82%B0%EC%97%85%ED%98%81%EB%AA%85".format(search=search)    
    driver = webdriver.Chrome("./chromedriver.exe")
    driver.get(url)
    time.sleep(2)
    
    etnewsUrlList(driver)

def etnewsUrlList(driver):
    url2 = driver.current_url
    for pageNo in range(1,212): #2페이지까지
        url = url2 + "&pageNum={pageNo}".format(pageNo=pageNo)
        driver.get(url)
        time.sleep(2)
        
        yonhapnewsUrs= driver.find_elements_by_css_selector(".list_news .clearfix dt a")
        yonhapnewsUrs_List = []    
        for urlList in yonhapnewsUrs:
            yonhapnewsUrs_List.append(urlList.get_attribute("href"))
        etnewsInfo(driver,yonhapnewsUrs_List)

def etnewsInfo(driver,yonhapnewsUrs_List):
    for urlList in yonhapnewsUrs_List:
        print("- url - : \n",urlList)
        try:
            driver.get(urlList)
            time.sleep(2)
            newsDate = driver.find_element_by_css_selector(".article_header_sub .date").text.replace("발행일 : ","").replace(".","")[0:8]
            newsTitle = driver.find_element_by_css_selector(".article_title").text
            newsSubtitles = driver.find_elements_by_css_selector("#articleBody h3")
            newsSubtitle_result = ""
            for newsSubtitle in newsSubtitles:
                newsSubtitle_result+=newsSubtitle.text
            newsContents = driver.find_elements_by_css_selector("#articleBody p")
            print("- 날짜 - : \n",newsDate)        
            print("- 기사 제목 - : \n",newsTitle)
    #        print("- 기사 부제목 - \n:",newsSubtitle_result)
    #        print("- 기사 본문 - \n")
            content_result = ""
            for content in newsContents:
                content_result+=content.text
    #        print(content_result)

            dbData = [[urlList,newsDate,newsTitle,newsSubtitle_result,content_result]]
            connectDB(dbData)
        except:
            alert = driver.switch_to_alert()
            alert.accept()
            print("로그인이 필요한 뉴스 입니다.")
            continue
        
def connectDB(dbData):
    DB_HOST = '127.0.0.1'
    DB_USER = 'root'
    DB_PASSWD = 'autoset'
    DB_NAME = 'python'
    
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWD,
                       db=DB_NAME, charset='utf8')
    curs = conn.cursor()

    sql = """insert into etnews(url,newsDate,newsTitle,newsSubtitle,content)
         values (%s, %s, %s, %s, %s)"""
    curs.executemany(sql,dbData)    
    conn.commit()
    conn.close()

search = "원자력"
전자신문(search)


