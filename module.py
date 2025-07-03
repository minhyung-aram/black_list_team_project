import pandas as pd
import joblib
import os
from model_final.XGBoost import extract_url_features
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
def load_blacklist():
    if not os.path.exists("blacklist.csv"):
        df = pd.Series([], name="url")
        df.to_csv("blacklist.csv")
    return pd.read_csv("blacklist.csv", names=["url"])

def save_csv(df):
    df.to_csv("blacklist.csv", index=False, header=False)

def model_call(url):
    model = joblib.load("model_final/XGBoost_model.pkl")

    features_dict = extract_url_features(url) # 변수명을 features_dict로 변경하여 혼동 방지
    features_array = np.array(list(features_dict.values())).reshape(1, -1)

    prediction = model.predict(features_array)

    return prediction[0]