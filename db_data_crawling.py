import time
import pandas as pd
import requests
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

""""
1. 해당 부분에서는 화면 밖에 내용을 보여주면 되기에, 큰 이미지까지는 필요없을거라고 판단하였음

수집 데이터  : text : title , 글쓴이 , 출판사, 판매가 
            url : 이미지 url , 상세정보창 url 

DB 저장 순서 : title , 지은이 , 출판사 , 키워드 , 이미지uri , 상세정보창uri 

text 먼저 수집 후 -> URi 수집

만약 키워드가 업었다면 beautifulsoup로 진행해도 되었지만 해당 부분 데이터를 저장할때
꼬일 수도있기에, 셀레니움으로 저장하는것이 더 안전하다 판단되었음 

구조 더 생각해보고 코드 수정해야할거같아보임 
"""

driver = webdriver.Chrome('./chromedriver')
driver.get('http://www.kyobobook.co.kr/categoryRenewal/categoryMain.laf?linkClass=0101&mallGb=KOR&orderClick=JAR')

image_count = 0
page_index = 1



def Data_get():
    Title = driver.find_element_by_xpath('//*[@id="container"]/div[2]/form/div[1]/h1/strong').text
    writer = driver.find_element_by_xpath('//*[@id="container"]/div[2]/form/div[1]/div[2]/span[1]/a').text
    book_made = driver.find_element_by_xpath('//*[@id="container"]/div[2]/form/div[1]/div[2]/span[3]/a').text
    sell_price = driver.find_element_by_xpath('//*[@id="container"]/div[2]/form/div[3]/div[1]/ul/li[1]/span[2]/strong').text
    image_uri = driver.find_element_by_xpath('//*[@id="container"]/div[2]/form/div[2]/div[1]/div/a/img').get_attribute('src')

    data_info = {"Title":Title, "Writer":writer, "Book_made":book_made,"sell_price":sell_price, "image_uri":image_uri}
    frame = pd.DataFrame([data_info])
    frame.to_csv('DB.csv', index_label='index', index=True)



def move():  # 셀레니움을 이용한 화면 이동
    global image_count, page_index
    for i in range(1, 40, 2):
        elem = driver.find_element_by_xpath(
            f'//*[@id="prd_list_type1"]/li[{i}]/div/div[1]/div[2]/div[1]/a')  # 각 path 접근
        elem.click()  # 접근한 path 타이틀 클릭 (상세페이지 접속)
        time.sleep(3)

        # 내용 채워야댐 (데이터 수집 내용)
        Data_get()

        if image_count == 20:
            page_index += 1
            next_page = driver.find_element_by_xpath(f'//*[@id="eventPaging"]/div/ul/li[{page_index}]/a')
            next_page.send_keys(Keys.ENTER)
            print(f'page index  : {page_index}')
            time.sleep(2)
            image_count = 0
            print(f'이미지 수집 개수 초기화 : {image_count}')


move()