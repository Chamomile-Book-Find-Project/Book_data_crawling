import time
import warnings
import pandas as pd
import os
import requests
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

""""
DB 저장 순서 : title , 지은이 , 출판사 , 이미지uri
"""

'''
      main 함수
    while문 (베스트셀러 목록 다음 페이지 버튼이 활성화 되어 있을 때)  
       for문: 각각 상세 페이지 접근(베스트셀러 한 페이지 내에서, 페이지 당 20권임)
            상세페이지  클릭         
             if아님 try문 (청불 판독): 팝업 창이 뜬다면 청불로 간주.
                청불일 시
                    0.팝업 확인 누르기
                    1.continue
                청불아닐 시    
                    0.데이터 겟 이용해 데이터 수집
                    1.뒤로가기
       다음 페이지!(베스트셀러 페이지 넘기기)

 '''

warnings.filterwarnings(action='ignore')

driver = webdriver.Chrome('C:/Users/choco/Desktop/quick/ai_chatbot/aaa/Book_data_crawling/jungmin/chromedriver.exe')
driver.get('http://www.kyobobook.co.kr/categoryRenewal/categoryMain.laf?pageNumber=1&perPage=50&mallGb=KOR&linkClass=0103&ejkGb=&sortColumn=near_date')

def data_get(): #각 정보의 path 이용해 불러오기

    title = driver.find_element_by_xpath('//*[@id="container"]/div[2]/form/div[1]/h1/strong').text

    try:
        writer = driver.find_element_by_xpath('//*[@id="container"]/div[2]/form/div[1]/div[2]/span[1]/a').text
    except:
        writer = driver.find_element_by_xpath('//*[@id="container"]/div[2]/form/div[1]/div[3]/span[1]/a').text
    try:
        book_made = driver.find_element_by_xpath('//*[@id="container"]/div[2]/form/div[1]/div[2]/span[5]/a').text
    except:
        book_made = driver.find_element_by_xpath('//*[@id="container"]/div[2]/form/div[1]/div[3]/span[5]/a').text

    ''' 
    중국소설 파트
    book_made_1tf = driver.find_element_by_xpath('//*[@id="container"]/div[2]/form/div[1]/div[2]/span[5]/a').is_displayed()
    book_made_2tf = driver.find_element_by_xpath('//*[@id="container"]/div[2]/form/div[1]/div[3]/span[5]/a').is_displayed()
    book_made_3tf = driver.find_element_by_xpath('//*[@id="container"]/div[2]/form/div[1]/div[2]/span[3]/a').is_displayed()
    book_made_4tf = driver.find_element_by_xpath('//*[@id="container"]/div[2]/form/div[1]/div[3]/span[3]/a').is_displayed()

    if (book_made_1tf == True):
        book_made = driver.find_element_by_xpath('//*[@id="container"]/div[2]/form/div[1]/div[2]/span[5]/a')
    elif (book_made_2tf == True):
        book_made = driver.find_element_by_xpath('//*[@id="container"]/div[2]/form/div[1]/div[3]/span[5]/a')
    elif (book_made_3tf == True):
        book_made = driver.find_element_by_xpath('//*[@id="container"]/div[2]/form/div[1]/div[2]/span[3]/a')
    elif (book_made_4tf == True):
        book_made = driver.find_element_by_xpath('//*[@id="container"]/div[2]/form/div[1]/div[3]/span[3]/a')'''

    try:
        sell_price = driver.find_element_by_xpath(
            '//*[@id="container"]/div[2]/form/div[3]/div[1]/ul/li[1]/span[2]/strong').text
    except:
        sell_price = driver.find_element_by_xpath(
            '//*[@id="container"]/div[2]/form/div[3]/div[1]/ul/li[1]/span[4]/strong').text

    try:
        image_uri = driver.find_element_by_xpath('//*[@id="container"]/div[2]/form/div[2]/div[1]/div/a/img').get_attribute('src')
    except:
        image_uri = driver.find_element_by_xpath('//*[@id="container"]/div[2]/form/div[2]/div[1]/div/img').get_attribute('src')

    data_info = {"Category":"영미소설", "Title":title, "Writer":writer, "Book_made":book_made,"Sell_price":sell_price, "Image_uri":image_uri}
    frame = pd.DataFrame([data_info])
    csv = 'DB_ENG.csv'
    if not os.path.exists(csv):
        frame.to_csv(csv, index=False, mode='w', encoding='utf-8-sig')
    else:
        frame.to_csv(csv, index=False, mode='a', encoding='utf-8-sig', header=False)


#베스트 셀러 목록 관련 세팅 (버튼 활성화 여부)
btn_next1 = driver.find_element_by_css_selector('#eventPaging > div > a')
btn_next2 = driver.find_element_by_css_selector('#eventPaging > div > a.btn_next')
next_page1 = btn_next1.is_displayed()
next_page2 = btn_next2.is_displayed()






def move():
    """
    셀레니움을 이용한 화면 이동
    """
    # 베스트 셀러 목록 관련 세팅 (버튼 활성화 여부)
    btn_next1 = driver.find_element_by_css_selector('#eventPaging > div > a')
    btn_next2 = driver.find_element_by_css_selector('#eventPaging > div > a.btn_next')
    next_page1 = btn_next1.is_displayed()
    next_page2 = btn_next2.is_displayed()

    ''' 
    오류 났을 때 사용(목록 페이지 이동)
    btn_next1.send_keys(Keys.ENTER)
    for j in range(1,3,1):
        btn_next2 = driver.find_element_by_css_selector('#eventPaging > div > a.btn_next')
        next_page2 = btn_next2.is_displayed()
        btn_next2.send_keys(Keys.ENTER)
    '''

    # 베스트 셀러 목록 (크롤링 할 범위 설정)
    book_num  = 0
    page = 1
    while ((next_page1 or next_page2) == True):
        # 상세 페이지 접속 관련
        for i in range(1, 100, 2):
            elem = driver.find_element_by_xpath(
                f'//*[@id="prd_list_type1"]/li[{i}]/div/div[1]/div[2]/div[1]/a')  # 각 path 접근
            elem.click()  # 접근한 path 타이틀 클릭 (상세 페이지 접속)

            # 청불 판독 및 청불 아닐 때 정보 수집
            try:  # 팝업 뜰 경우(청불), 확인 누르고 continue
                WebDriverWait(driver, 1).until(ec.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                
            except:  # 팝업 안뜰 때(청불x), 정보 받고 이전 페이지로 이동
                data_get()
                driver.back()
                if book_num != 50:
                    book_num += 1
                else:
                    book_num = 1
                print(book_num, "번째 책  ")

        # 베스트 셀러 목록 관련 세팅 (버튼 활성화 여부)
        btn_next1 = driver.find_element_by_css_selector('#eventPaging > div > a')
        btn_next2 = driver.find_element_by_css_selector('#eventPaging > div > a.btn_next')
        next_page1 = btn_next1.is_displayed()
        next_page2 = btn_next2.is_displayed()

        time.sleep(1)
        if (page==1):
            btn_next1.send_keys(Keys.ENTER)
            page += 1
            print("     <페이지: ", page,">")
        else:
            btn_next2.send_keys(Keys.ENTER)
            page += 1
            print("     <페이지: ", page,">")
        time.sleep(1)
    
    driver.quit()
move()