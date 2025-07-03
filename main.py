import json
import openai
from dotenv import load_dotenv
import os
import importlib

load_dotenv()

OPEN_API_KEY = os.getenv("OPEN_API_KEY")

client = openai.OpenAI(api_key=OPEN_API_KEY)

tools = [{
    "type": "function",
    "name": "check_black_list",
    "description": "사용자로부터 악성 url 관련 판단 질문을 받으면 ML모델을 사용하여 악성 url 판단결과를 받는 함수입니다.",
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
                "output": e
            })
    return result

context = []
context.append({
    "role" : "system",
    "content" : "악성코드에 대한 질문이 들어오면 function call을 이용해 응답을 받아야합니다.\
        1이면 악성 url이며 0이면 정상url입니다. 추가로 url이 악성이면 사용자가 보낸 domain을 통해\
            사용자의 url 진입목적을 유추해 websearch를 통해 대안사이트를 3~4가지 url과 함께 제시해줍니다."
})
user_prompt = input("무엇을 도와드릴까요?")

context.append({"role" : "user", "content" : user_prompt})
response = client.responses.create(
    model="gpt-4.1",
    input=context,
    tools=tools,
    tool_choice="auto"
)

answer = function_call(response.output)
context.extend(answer)

final_response = client.responses.create(
    model="gpt-4.1",
    input=context,
    tools=tools,
    tool_choice="auto")

print(final_response.output_text)