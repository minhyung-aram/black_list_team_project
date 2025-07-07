# black_list_team_project
sk 쉴더스 AI 26기 1차 모듈프로젝트입니다.


====================================================================
# PhishingGuard Chat 사용 설명서
1. 파일 구성
파일명
역할 요약
Home.py
Streamlit 기반 웹 인터페이스
agent.py
상위 에이전트 클래스 (대화 흐름 관리 및 Function Call 처리)
main.py
단독 실행 가능 CLI 인터페이스
module.py
URL 블랙리스트 검사 및 ML모델 예측
preprocess.py
URL 전처리 기능
vector_store.py
OpenAI 벡터스토어 및 파일 업로드 기능
XGBoost_model.pkl
XGBoost 모델 훈련 및 평가



2. 설계 구조
<img width="1243" height="591" alt="Image" src="https://github.com/user-attachments/assets/446a15b1-b974-41b8-91a2-3abaf82ed03a" />



3. 사용 툴
툴
역할 요약
websearch_preview
사용자와의 일반적인 대화나 악성 url로 인한 대안사이트를 찾는 websearch
file_search
하위 에이전트에게 악성 url에 대한 전문적인 지식을 주기위한 file_search
function_call
악성 url 관련 질문을 받았을 때 사용할 function_call 



4. 호출 함수
agent_call : 메인 에이전트가 악성 URL 관련 질문을 받았을 때 호출하는 함수입니다.
해당 호출 함수는 블랙리스트 검사 및 하위 에이전트 호출을 담당합니다.

5. 모델 학습/사용법
XGBoost 모델을 사용하며, 모델 학습 방법은 다음과 같습니다.

URL 컬럼이 있는 csv 데이터 셋을 준비한다.
XGBoost.py에서 파일 경로를 해당 csv 데이터 셋으로 바꾼다.
XGBoost.py를 실행한다.
.pkl 파일이 저장된다.

이후, 모델 사용 예시 코드는 다음과 같습니다.
<img width="1167" height="468" alt="Image" src="https://github.com/user-attachments/assets/d05ea2ce-358a-4166-a440-d2fc9bd253d3" />


6. 에이전트 상호작용
<img width="1236" height="767" alt="Image" src="https://github.com/user-attachments/assets/66fe3c79-303c-40c3-839b-0a910bcd00f6" />
<img width="1236" height="797" alt="Image" src="https://github.com/user-attachments/assets/95c7bcc2-bf6c-4b8e-bd23-745cb223e326" />
<img width="1236" height="515" alt="Image" src="https://github.com/user-attachments/assets/545d6c06-a2de-4ef6-a590-5273967ae899" />

7. 사용자 가이드
https://github.com/minhyung-aram/black_list_team_project.git, git clone하기
requirements.txt를 사용하여 종속 라이브러리 다운로드
따로 준비한 데이터 셋이 있을 경우 (5)의 내용을 토대로 학습하고 저장하기
module.py의 model_call 함수에서 .pkl 파일 경로 설정
커맨드라인에 streamlit run Home.py를 하여 streamlit 웹 실행


8. 예시 시나리오 및 응답
<img width="727" height="463" alt="Image" src="https://github.com/user-attachments/assets/066d1061-ade9-49a1-b287-a800de9b3b5d" />
<img width="727" height="551" alt="Image" src="https://github.com/user-attachments/assets/50c3fe07-8dd7-4f99-bbe0-dbd4d65acb29" />

