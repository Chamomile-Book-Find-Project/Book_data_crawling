"""
1. 이미지 크롤링을 진행하여 해당 이미지들을 먼저 전달하기
2. DB에 저장할 내용들 크롤링 진행
"""

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request


def image_get():
    driver = webdriver.Chrome('./chromedriver')
    driver.get('http://www.kyobobook.co.kr/categoryRenewal/categoryMain.laf?linkClass=0101&mallGb=KOR&orderClick=JAR')
    for i in range(1,40,2):
        elem = driver.find_element_by_xpath(f'//*[@id="prd_list_type1"]/li[{i}]/div/div[1]/div[2]/div[1]/a')  # 각 path 접근
        elem.click()  # 접근한 path 타이틀 클릭 (상세페이지 접속)
        time.sleep(2)
        book_image = driver.find_element_by_xpath('//*[@id="container"]/div[2]/form/div[2]/div[1]/div/a/img') # 책 이미지를 크게 저장하기위한 이미지 클릭
        book_image.click()
        time.sleep(2) #여기까진 성공


image_get()