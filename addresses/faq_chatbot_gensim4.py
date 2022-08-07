import os
#from gensim.models import doc2vec # gensim4에서 사라짐
from gensim.models.doc2vec import TaggedDocument, Doc2Vec # gensim4에서 추가됨
import pandas as pd
#import openpyxl
#import datetime
import pymysql.cursors

# 모델 불러오기 # gensim3이랑 gensim4랑 모델 호환 안 되어서 다시 만들어야 함
d2v_faqs = Doc2Vec.load(os.path.join('./model/d2v_faqs_size200_min5_epoch20_ebs_science_qna_gensim4.model')) # gensim4 스타일로 변경

# 질문-답변 파일 불러오기
df2 = pd.read_excel('./data/df2_20220805_edited.xlsx')
df2.dropna(axis=0)

qna_num = 0  # 질문답변 번호인 qna_num 초기화

# Mecab 사용
from konlpy.tag import Mecab

mecab = Mecab()
text = u"""이제 구글 코랩에서 Mecab-ko 라이브러리 사용이 가능합니다. 읽어주셔서 감사합니다. 펭수"""
nouns = mecab.nouns(text)
print(nouns)

filter_mecab = ['NNG',  # 보통명사
                'NNP',  # 고유명사
                'SL',  # 외국어
                'VV',  # 동사 추가함 (20200831)
                'VA',  # 형용사 추가함 (20200831)
                'NP',  # 대명사 추가함 (20200928)
                'NR',  # 수사 추가함 (20200929)
                'SN',  # 숫자 추가함 (20200929)
                #'MAG' # 일반부사 추가함 (20210405, 20210531에 다시 제외함)
                ]


def tokenize_mecab(doc):
    # jpype.attachThreadToJVM()
    token_doc = ['/'.join(word) for word in mecab.pos(doc)]
    return token_doc


def tokenize_mecab_noun(doc):
    # jpype.attachThreadToJVM()
    token_doc = ['/'.join(word) for word in mecab.pos(doc) if word[1] in filter_mecab]
    return token_doc


index_questions = []

for i in range(len(df2)):  # df2가 0부터 시작
    index_questions.append([tokenize_mecab_noun(df2['질문'][i]), i])  # 명사만 추출

# Doc2Vec에서 사용하는 태그문서형으로 변경
tagged_questions = [TaggedDocument(d, [int(c)]) for d, c in index_questions]


# FAQ 답변
def faq_answer(input, useragent, client_ip):
    if len(input) < 6:
        return '질문이 너무 짧아요. 좀 더 구체적으로 질문 부탁해요.'
    else:
        # 테스트하는 문장도 같은 전처리를 해준다.
        tokened_test_string = tokenize_mecab_noun(input)

        topn = 1  # 가장 유사한 질문 한 개까지만
        test_vector = d2v_faqs.infer_vector(tokened_test_string)
        result = d2v_faqs.docvecs.most_similar([test_vector], topn=topn)

        for i in range(topn):
            print("유사질문 {}위 | 유사도: {:0.3f} | 문장 번호: {} | {}".format(i + 1, result[i][1], result[i][0], df2['질문'][result[i][0]]))
            # print("\t질문 {} | 문장 번호: {} | {}".format(i + 1, result[i][0], df2['답변'][result[i][0]]))
            # print(len(df2['답변'][result[i][0]]))
            # for j in range(len(df2['답변'][result[i][0]])):
            #    #print(j)
            #    print("\t질문 {} | 답글순서 {} | 문장 번호: {} | {}".format(i + 1, j + 1, result[i][0], df2['답변'][result[i][0]][j]))

            # 시각과 사용 운영체제, 입출력 데이터 엑셀로 저장 (20210227부 데이터베이스에 저장. 엑셀은 데이터 양이 많아지면 저장만 5초 이상 걸리는 문제가 생겼음)
            #now = datetime.datetime.now()
            #nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
            #load_wb = openpyxl.load_workbook('/home/ubuntu/faq_chatbot_science_3rd/data/datalog.xlsx', data_only=True)
            #load_ws = load_wb['Sheet']
            #time_and_input_output = [nowDatetime, useragent, result[i][1], input, df2['질문'][result[i][0]], df2['답변'][result[i][0]]]
            # 질문이 입력된 시각, 유사도, 질문 내용, 가장 유사한 질문, 답변을 저장
            #load_ws.append(time_and_input_output)  # 엑셀 파일에 차곡차곡 누가기록
            #load_wb.save('/home/ubuntu/faq_chatbot_science_3rd/data/datalog.xlsx')

            # 질문 입력 시 정보를 데이터베이스에 저장
            connection = pymysql.connect(host='127.0.0.1', user='test', password='3014', db='chatbot_datalog', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
            with connection.cursor() as cursor:
                sql = """INSERT INTO datalog (client_ip, useragent, similarity, student_question, dataset_question, answer)
                         VALUES ('%s', '%s', '%f', '%s', '%s', '%s')"""%(client_ip, useragent, result[i][1], input, df2['질문'][result[i][0]], df2['답변'][result[i][0]])
                cursor.execute(sql)
            connection.commit()
            connection.close()
            print(client_ip)
            if result[i][1] < 0.6:
                return '입력한 질문에 대한 가장 유사한 질문의 유사도가 {:0.1f}%라서 60% 미만이라 엉뚱한 소리를 할 것 같으니 결과를 출력하지 않을게요. 질문을 더 구체적으로 써 주세요.'.format(result[i][1] * 100)
            else:
                return '입력한 질문과의 유사도: {:0.1f}%<br/><br/>질문: '.format(result[i][1] * 100) + df2['질문'][result[i][0]] + '<br/><br/>답변: ' + df2['답변'][result[i][0]]

print('챗봇 불러오기 완료')
