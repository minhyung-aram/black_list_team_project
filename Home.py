import json, openai, os, importlib, streamlit as st
from dotenv import load_dotenv

# 환경변수 불러오기 및 OpenAI API Key 설정
load_dotenv()
OPEN_API_KEY = os.getenv("OPEN_API_KEY")
client = openai.OpenAI(api_key=OPEN_API_KEY)

# 함수 설정
tools = [{
    "type": "function",
    "name": "check_black_list",
    "description": "사용자로부터 악성 URL 관련 판단 질문을 받으면 ML모델을 사용하여 악성 URL 판단결과를 받는 함수입니다.",
    "parameters": {
        "type": "object",
        "properties": {
            "url": {"type": "string"}
        },
        "required": ["url"],
        "additionalProperties": False
    },
    "strict": True
},
{
    "type": "web_search_preview"
}
]

def function_call(calls):
    result = []
    for call in calls:
        if call.type != "function_call":
            continue   
        try :
            result.append(call)
            function_modules = importlib.import_module("module")
            function_name = call.name
            func = getattr(function_modules, function_name)
            function_args = json.loads(call.arguments)
            output = func(**function_args)
            result.append({
                "call_id": call.call_id,
                "type": "function_call_output",
                "output": str(output)
            })

        except Exception as e:
            result.append({
                "call_id": call.call_id,
                "type": "function_call_output",
                "output": str(e)
            })
    return result

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

    context = [{
        "role" : "system",
        "content" : "악성코드에 대한 질문이 들어오면 Function call을 이용해 응답을 받아야 합니다.\
        1이면 악성 URL이며 0이면 정상 URL입니다. 추가로 URL이 악성이면 사용자가 보낸 도메인을 통해\
        사용자의 URL 진입목적을 유추하고 Websearch를 통해 대안사이트를 3~4개의 URL과 함께 제시해줍니다."
    }]
    context.append({'role' : 'user', 'content' : user_prompt})
    response = client.responses.create(
        model="gpt-4o",
        input=context,
        tools=tools,
        tool_choice="auto"
    )

    # Function Call 처리
    answer = function_call(response.output)
    context.extend(answer)

    final_response = client.responses.create(
        model="gpt-4o",
        input=context,
        tools=tools,
        tool_choice="auto")

    # AI 응답 출력
    with st.chat_message('assistant') :
        st.markdown(final_response.output_text)

    st.session_state.messages.append({
        'role' : 'assistant',
        'content' : final_response.output_text
    })

