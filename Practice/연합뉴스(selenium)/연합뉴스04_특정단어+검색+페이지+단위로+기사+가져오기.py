from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def yonhapnewsUrl(search):
    url = "http://www.yonhapnews.co.kr/home09/7091000000.html?query={search}&ctype=A".format(search=search)
    driver = webdriver.Chrome("./chromedriver.exe")
    driver.get(url)
    
    return yonhapnewsUrlList(driver)

def yonhapnewsUrlList(driver):
    url2 = driver.current_url
    yonhapnewsUrs_List = []
    for pageNo in range(1,2): #1페이지까지
        url = url2 + "&page_no={pageNo}".format(pageNo=pageNo)
        driver.get(url)
        
        yonhapnewsUrs= driver.find_elements_by_css_selector(".cts_atclst li a")
    
        for urlList in yonhapnewsUrs:
            yonhapnewsUrs_List.append(urlList.get_attribute("href"))
    return yonhapnewsInfo(driver,yonhapnewsUrs_List)

def yonhapnewsInfo(driver,yonhapnewsUrs_List):
    for urlList in yonhapnewsUrs_List:
        driver.get(urlList)
        newsTitle = driver.find_element_by_css_selector(".tit-article").text
        newsSubtitles = driver.find_elements_by_css_selector(".stit strong")
        newSubtitle_result = ""
        for newsSubtitle in newsSubtitles:
            newSubtitle_result+=newsSubtitle.text
        newsContents = driver.find_elements_by_css_selector(".article p")
        print("- 기사 제목 - : \n",newsTitle)
        print("- 기사 부제목 - \n:",newSubtitle_result)
        print("- 기사 본문 - \n")
        for content in newsContents:
            print(content.text,end=" ")

search = input("검색 : ")
yonhapnewsUrl(search)

