import tensorflow as tf
import os
import pandas as pd
import pymysql.cursors
import numpy as np
from numpy import dot
from numpy.linalg import norm

# SBERT 불러오기
from sentence_transformers import SentenceTransformer

# 질문 데이터로 SBERT 학습한 모델 불러오기
model = SentenceTransformer('./model/sbert_qna_3.model')

# 학습시켜서 얻은 임베딩 값 입력된 데이터프레임 불러오기
train_data = pd.read_pickle('./data/train_data_SBERT_3.pkl')
train_data = train_data[['번호', '질문', '답변', 'embedding']]

qna_num = 0  # 질문답변 번호인 qna_num 초기화

#두 개의 벡터로부터 코사인 유사도를 구하는 함수 cos_sim를 정의합니다.

def cos_sim(A, B):
    return dot(A, B)/(norm(A)*norm(B))

#return_answer 함수는 임의의 질문이 들어오면 해당 질문의 문장 임베딩 값과 챗봇 데이터의 임베딩 열.
#즉, train_data['embedding']에 저장해둔 모든 질문 샘플들의 문장 임베딩 값들을 전부 비교하여
#코사인 유사도 값이 가장 높은 질문 샘플을 찾아냅니다. 그리고 해당 질문 샘플과 짝이 되는 답변 샘플을 리턴합니다.

def return_answer(question):
    embedding = model.encode(question)
    train_data['score'] = train_data.apply(lambda x: cos_sim(x['embedding'], embedding), axis=1)
    return train_data.loc[train_data['score'].idxmax()]['답변']

# FAQ 답변
def faq_answer(input, useragent, client_ip, uuid):
    if len(input) < 6:
        return '질문이 너무 짧아요. 좀 더 구체적으로 질문 부탁해요.'
    else:
        # 테스트하는 문장도 같은 전처리를 해준다.

        topn = 1  # 가장 유사한 질문 한 개까지만
        result = return_answer(input)
        most_sim_answer_largest = train_data.nlargest(topn, "score")

        for i in range(topn):
            print("유사질문 {}위 | 유사도: {:0.3f} | 문장 번호: {} | {}".format(i+1, most_sim_answer_largest.iloc[i]['score'], most_sim_answer_largest.iloc[i]['질문'], most_sim_answer_largest.iloc[i]['번호']))

            # 질문 입력 시 정보를 데이터베이스에 저장
            connection = pymysql.connect(host='152.70.234.27', user='test', password='3014', db='chatbot_datalog', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
            with connection.cursor() as cursor:
                sql = """INSERT INTO datalog (client_ip, uuid, useragent, similarity, student_question, dataset_question, answer)
                         VALUES ('%s', '%s', '%s', '%f', '%s', '%s', '%s')"""%(client_ip, uuid, useragent, most_sim_answer_largest.iloc[i]['score'], input, most_sim_answer_largest.iloc[i]['질문'], result)
                cursor.execute(sql)
            connection.commit()
            connection.close()
            if most_sim_answer_largest.iloc[i]['score'] < 0.6:
                return '입력한 질문에 대한 가장 유사한 질문의 유사도가 {:0.1f}%라서 60% 미만이라 엉뚱한 소리를 할 것 같으니 결과를 출력하지 않을게요. 질문을 더 구체적으로 써 주시거나 다른 질문을 해 주시면 제가 답변드릴 기회를 얻을 수 있을 것 같아요.'.format(most_sim_answer_largest.iloc[i]['score'] * 100)
            else:
                return '입력한 질문과의 유사도: {:0.1f}%<br/><br/>질문: '.format(most_sim_answer_largest.iloc[i]['score'] * 100) + most_sim_answer_largest.iloc[i]['질문'] + '<br/><br/>답변: ' + result

print('챗봇 불러오기 완료')
