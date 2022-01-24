"""
1. 이미지 크롤링을 진행하여 해당 이미지들을 먼저 전달하기
2. DB에 저장할 내용들 크롤링 진행
"""
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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

        book_title_1 = driver.find_element_by_xpath('//*[@id="container"]/div[2]/form/div[1]/h1/strong')
        book_title_2 = book_title_1.text
        time.sleep(2)
        driver.switch_to.frame('UXModalIframe')  # 프레임 전환 하여 이미지 상세창으로 이동

        book_url = driver.find_element_by_xpath(
            '/html/body/table/tbody/tr/td/table[2]/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody/tr[1]/td[1]/table/tbody/tr/td/img').get_attribute(
            'src')

        urllib.request.urlretrieve(book_url, f'./book_image/{book_title_2}.jpg')  # 이미지 저장
        time.sleep(3)

        back_botton = driver.find_element_by_xpath(
            "/html/body/table/tbody/tr/td/table[1]/tbody/tr/td[3]/a")  # x 버튼 이미지 path 탐색
        back_botton.send_keys(Keys.ENTER)  # 해당 path에 있는 버튼 클릭
        time.sleep(3)

        # 오류 생성부분
        driver.switch_to.default_content()  # 해당 프레임 빠져나가기
        driver.back()
        driver.back()
        time.sleep(3)


image_get()
