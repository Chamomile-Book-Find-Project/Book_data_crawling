# Book_data_crawling

# 목표
교보문고 각 카테고리 별 이미지, 이미지url , title , 작가 , 출판사 , 한줄평 데이터 수집 <br> 
<br>
<br>
<br>
# 현재까지 진행상황 

1/20 : 기본적인 접근 및 크롤링 단계 구조화 완료 
<br>
1/21 : 기본적인 이미지 접근 및 이미지 수집 폴더 생성 + 다운 코드 작성 
<br> 
1/22 : 이미지 다운 문제 해결 + 전반적인 진행 흐름 재설정 
<br> 
1/23 : Frame을 빠져나와 상세화면으로 돌아가기 설정 완료 
<br>
1/24 : 전반적인 리팩토링, 한 페이지의 이미지들 크롤링 작업화 완료 

<br>

# 문제점 
1/21 이미지 path 접근까지 완료하였는데 이미지 수집이 진행되지 않고 없는 요소라고 에러가 뜸 
<br> 
1/23 이미지 수집 후, 창을 닫고 이전 화면으로 돌아가고 싶은데, Frame 설정을 해제해 줘도 driver.back()이 작동하지 않음  
# 해결
1/22 : 각 웹 페이지안에 페이지를 띄운형태로 존재하여 dirver.switch_to.frame을 이용해 해당 frame으로 접근을 시도해야했음 
<br>
1/24 : 상세보기 이동으로 인한 history가 중첩되어 있는것으로 추정됨, 2번을 하니 뒤로가기가 제대로 작동이 되었음 
