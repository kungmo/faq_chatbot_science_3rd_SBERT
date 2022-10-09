from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

# Chrome의 경우 | 아까 받은 chromedriver의 위치를 지정해준다.
# driver = webdriver.Chrome('C:/WinPython37F/notebooks/faq_chatbot_science_3rd/data/chromedriver.exe') # Windows에서 사용
driver = webdriver.Chrome('/Users/kungmo/Downloads/chromedriver') # 맥에서 사용
# Mac 경로: /Users/kungmo/Downloads/chromedriver
# Linux에서 Firefox 사용:
# driver = webdriver.Firefox(executable_path='/home/kungmo/다운로드/geckodriver')
#driver.implicitly_wait(10) # 5초 대기
page_num = 2 # 10개 질문 모두 답변이 들어 있는 첫 번째 페이지 번호
last_page_num = 80 # EBS 데이터 모을 마지막 페이지 번호
qna_num = 0 #질문답변 세트 번호인 qna_num 초기화
df2 = pd.DataFrame(columns=['질문', '답변']) # qnas에서 질문에 해당하는 답변을 한 세트로 묶어 df2에 저장하려고 빈 데이터프레임을 만든다.

for i in range(last_page_num - page_num):
    url = 'https://mid.ebs.co.kr/course/view?courseId=10203440#qna/list/20001283/' + str(page_num + i) + '///0/titleContent//N//'
    driver.get(url)
    time.sleep(2) # 2초 대기

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser') # BeautifulSoup사용하기
    qnas = soup.select('.question_inner') # http://hleecaster.com/python-web-crawling-with-beautifulsoup/ 참고

    for qna in qnas: # 한 줄씩 번갈아가면서 질문-답변이 이어져서 리스트가 들어온 순서로 질문과 답변을 구분하여 데이터프레임에 집어 넣는다.
        if qnas.index(qna)%2 == 0:
            qna_num = qna_num + 1  # 이 줄 때문에 데이터프레임에 질문과 답변이 1번부터 들어감
            if not qna.text.strip(): # 질문이 비어 있으면
                df2.at[qna_num, '질문'] = '질문 내용 없음'
            else:
                df2.at[qna_num, '질문'] = qna.text.strip()  # 데이터프레임에 질문 입력
        else:
            df2.at[qna_num, '답변'] = qna.text.strip()
            df2.dropna(axis=0)

# 질문-답변 순서 뒤집히는 부분 발견
# 105쪽의 1번 문제 질문입니다! 여기에서 힘의 크기를 구하는 방법을 잘 모르겠어요ㅠ 이런 질문에서 순서 뒤바뀜 (6개 질문 정도만)
# 질문 속에 질문이 들어가 있어서 오류남. 수동으로 고쳐야 함.
# https://mid.ebs.co.kr/course/view?courseId=10203440#qna/list/20001283/99///0/titleContent//N// 에 있음.

df2.dropna(axis=0)
driver.quit()
#print(df2)

file_name = 'df2_20210207_EBS_보충'
df2.to_excel('{}.xlsx'.format(file_name))
print('{}.xlsx'.format(file_name))