from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymysql
import re
import time

def newsis(search) :
    driver = webdriver.Chrome("./chromedriver.exe")
    url = "http://www.newsis.com/search/schlist/?val={}&sort=acc&jo=all_jogun&bun=all_bun&sdate=&term=allday&edate=&s_yn=Y&catg=1&t=1&page=1&".format(search)
    driver.get(url)
    time.sleep(2)
    
    newsispage(driver)

def newsispage(driver) :
    currenturl = driver.current_url

    for pageNo in range(1,12) :
        urlLists = []
        url2 = currenturl + "&page={}".format(pageNo)
        driver.get(url2)
        time.sleep(2)
        
        hrefplace = driver.find_elements_by_css_selector(".txt1 a")
        for urlList in hrefplace:
            urlLists.append(urlList.get_attribute("href"))
              
        newsisinfo(driver,urlLists)        
        
def newsisinfo(driver,urlLists) :
    for urlList in urlLists :
        driver.get(urlList)

        newsDates = driver.find_elements_by_css_selector(".date")
        newsDate = newsDates[1].text
        newsDate = newsDate[3:13].replace("-","")
        print("==날짜== \n", newsDate)
        
        newsTitle = driver.find_element_by_css_selector(".article_tbx.mgt8.w970 h1").text
        print("==제목== \n", newsTitle)

        newsSubtitle =""
        
        newsContent = driver.find_element_by_css_selector("#textBody").text
        imgcapption= driver.find_elements_by_css_selector(".desc")
        
        if imgcapption == [] :
            pass
        elif len(imgcapption) == 1 :
            newsContent = newsContent.replace(imgcapption[0].text,"")
        else :
            imgcapption= driver.find_elements_by_css_selector(".desc")
            for cpation in imgcapption :
                newsContent = newsContent.replace(cpation.text,"")
        
        end_point = newsContent.rfind("@")
        newsContent = newsContent[0:end_point-7]
        datesCompile = re.compile(r'【\w\w=뉴시스】')
        pattern = datesCompile.findall(newsContent)
        pattern = str(pattern).replace("[","").replace("]","").replace("'","")
        
        newsContent = newsContent.replace(pattern,"")
        newsContent = newsContent[8: ]
        print("==내용== \n", newsContent)

        
        dbData = [[urlList,newsDate,newsTitle,newsSubtitle,newsContent]]
        connectDB(dbData)
        

def connectDB(dbData):
    DB_HOST = '127.0.0.1'
    DB_USER = 'root'
    DB_PASSWD = 'autoset'
    DB_NAME = 'python'
    
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWD,
                       db=DB_NAME, charset='utf8')
    
    curs = conn.cursor()

    sql = """insert into newsis(url,newsDate,newsTitle,newsSubtitle,content)
         values (%s, %s, %s, %s, %s)"""
    curs.executemany(sql,dbData)
    
    conn.commit()

    conn.close()


search = "웹툰"
newsis(search)

