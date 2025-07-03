<<<<<<< HEAD
import pandas as pd
import joblib
import os
from preprocess import extract_url_features
import numpy as np

def check_black_list(url):
    '''
    사용자로부터 url을 받았을 때 블랙리스트를 검사하고 
    블랙리스트에 없으면 ML 모델을 통해 검사하고 결과를 주는 함수입니다.
    '''
    black_list_df = load_blacklist()    
    if not black_list_df.empty:
        black_list = black_list_df['url'].tolist()
    else:
        black_list = []

    if url in black_list:
        return "해당 url은 블랙리스트에 존재하여 악성코드입니다."  
      
    check_t_f = model_call(url)
    
    if check_t_f:
        black_list.append(url)
        
        df = pd.Series(black_list, name="url").to_frame()
        save_csv(df)
        
        return check_t_f
    else:
        return check_t_f
    
# blacklist가 있는지 확인
=======
import joblib, os, pandas as pd, streamlit as st, numpy as np
from preprocess import extract_url_features

# 블랙리스트 파일 존재 확인
>>>>>>> ab1b090fb6230e7d8a646983a0e3912ee63b347c
def load_blacklist():
    if not os.path.exists("blacklist.csv"):
        df = pd.Series([], name="url")
        df.to_csv("blacklist.csv")
    return pd.read_csv("blacklist.csv", names=["url"])

<<<<<<< HEAD
def save_csv(df):
    df.to_csv("blacklist.csv", index=False, header=False)

def model_call(url):
    model = joblib.load("XGBoost_model.pkl")

    features_dict = extract_url_features(url) 
    features_array = np.array(list(features_dict.values())).reshape(1, -1)

    prediction = model.predict(features_array)

    return prediction[0]

=======
def check_black_list(url):
    '''
    사용자로부터 URL을 받았을 때 블랙리스트를 검사하고 
    블랙리스트에 없으면 ML 모델을 통해 검사하고 결과를 주는 함수입니다.
    '''
    black_list_df = load_blacklist() # 블랙리스트 불러오기

    # 블랙리스트가 비어있지 않다면
    if not black_list_df.empty:
        black_list = black_list_df['url'].tolist()
    # 비어있다면
    else:
        black_list = []

    # 블랙리스트에 존재하면 return
    if url in black_list:
        return "해당 URL은 블랙리스트에 존재하는 악성 URL입니다."
    # 블랙리스트에 존재하지 않으면 모델 부르기
    check_t_f = model_call(url)
    # 악성 url이면
    if check_t_f:
        # 블랙리스트에 추가
        black_list.append(url)
        # df로 만들어서
        df = pd.Series(black_list, name="url").to_frame()
        # csv로 저장
        save_csv(df)
        # 결과 반환하기
        return check_t_f
    # 정상이면
    else:
        return check_t_f

# 데이터프레임을 csv로 저장하는 함수
def save_csv(df):
    df.to_csv("blacklist.csv", index=False, header=False)

# 모델을 호출하여 결과를 반환받는 함수
def model_call(url):
    # pkl 파일 불러오기
    model = joblib.load("XGBoost_model.pkl")

    # url 전처리하기
    features_dict = extract_url_features(url)
    # 2차원으로 바꾸기 (모델에 넣기 위해)
    features_array = np.array(list(features_dict.values())).reshape(1, -1)
    # 모델 결과 받기
    prediction = model.predict(features_array)

    return prediction[0]
>>>>>>> ab1b090fb6230e7d8a646983a0e3912ee63b347c
