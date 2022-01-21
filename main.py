"""
1. 이미지 크롤링을 진행하여 해당 이미지들을 먼저 전달하기
2. DB에 저장할 내용들 크롤링 진행
"""
import os
from selenium import webdriver
import time
import urllib.request

image_folder = './book_image'

if not os.path.isdir(image_folder):
    os.mkdir(image_folder)
else:
    print('해당 폴더가 존재합니다.')


def image_get():
    driver = webdriver.Chrome('./chromedriver')
    driver.get('http://www.kyobobook.co.kr/categoryRenewal/categoryMain.laf?linkClass=0101&mallGb=KOR&orderClick=JAR')
    for i in range(1, 40, 2):
        elem = driver.find_element_by_xpath(
            f'//*[@id="prd_list_type1"]/li[{i}]/div/div[1]/div[2]/div[1]/a')  # 각 path 접근
        elem.click()  # 접근한 path 타이틀 클릭 (상세페이지 접속)
        time.sleep(3)

        book_image_botton = driver.find_element_by_xpath(
            '//*[@id="container"]/div[2]/form/div[2]/div[1]/div/a/img')  # 책 이미지를 크게 저장하기위한 이미지 클릭
        book_image_botton.click()
        time.sleep(3)  # 여기까진 성공

        book_url = driver.find_element_by_xpath(
            '/html/body/table/tbody/tr/td/table[2]/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody/tr[1]/td[1]/table/tbody/tr/td/img').get_attribute(
            'src')  # 책 이미지 path url 가져오기
        count = 1  # 책 이름 (가제)
        urllib.request.urlretrieve(book_url, str(count) + ".jpg")  # 이미지 저장 근데 왜안됨...
        time.sleep(3)

        back_botton = driver.find_element_by_xpath(
            "/html/body/table/tbody/tr/td/table[1]/tbody/tr/td[3]/a/img")  # x 버튼 이미지 path 탐색
        back_botton.click()  # 해당 버튼 클릭
        driver.back()  # 상세 페이지에서 뒤로가기


image_get()
