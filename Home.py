import json, openai, os, importlib, streamlit as st
from dotenv import load_dotenv
from agent import Agent

# 환경변수 불러오기 및 OpenAI API Key 설정
load_dotenv()
OPEN_API_KEY = os.getenv("OPEN_API_KEY")
client = openai.OpenAI(api_key=OPEN_API_KEY)

# Streamlit UI
st.title('PhishGuard Chat')
st.text('악성 URL을 판별하고 안전한 대안을 안내해주는 AI 보안 챗봇 서비스가 오픈되었습니다! 🎉')

# 대화 기록 초기화
if 'messages' not in st.session_state :
    st.session_state.messages = []

# 기존 메세지 출력
for msg in st.session_state.messages :
    with st.chat_message(msg['role']) :
        st.markdown(msg['content'])

# 사용자 입력
user_prompt = st.chat_input("무엇을 도와드릴까요?")

# GPT 응답 처리
if user_prompt :
    st.session_state.messages.append({'role' : 'user', 'content' : user_prompt})
    with st.chat_message('user') :
        st.markdown(user_prompt)
        
    with st.spinner("GPT 판단 중..."):
        agent = Agent(client)
        response = agent.chat(user_prompt)

    # AI 응답 출력
    with st.chat_message('assistant') :
        st.markdown(response)

    st.session_state.messages.append({
        'role' : 'assistant',
        'content' : response
    })

