import json, openai, os
from dotenv import load_dotenv
from module import check_black_list
from vector_store import vector_store_with_file

load_dotenv()
OPEN_API_KEY = os.getenv("OPEN_API_KEY")
client = openai.OpenAI(api_key=OPEN_API_KEY)

def agent_call(url):
    client = openai.OpenAI(api_key=OPEN_API_KEY)
    store_id = vector_store_with_file(
        "./악성url관련자료.pdf",
        "knowledge_base",
        client
    )

    if url:
        result = check_black_list(url)
        client = openai.OpenAI(api_key=OPEN_API_KEY)
        input = [{
            "role" : "system",
            "content" : "당신은 악성 URL 결과를 잘 리포팅해서 상위 에이전트에게 전달하는 역할을 합니다.\
                당신은 블랙리스트에 존재한다는 문자나 0 또는 1을 받습니다. 블랙리스트에 존재하면 악성 URL입니다.\
                0이면 정상 URL, 1이면 악성 URL을 뜻하고 이는 ML모델에 넣은 결과입니다. 정상 URL은 그냥 상위 에이전트에게 정상이라고 전달하면 되고\
                악성 URL이면 벡터 스토어의 파일에는 악성 URL에 대한 자료가 있는데 이걸로 해당 URL에 대한 정보를 가져오는게 아니라\
                왜 악성 URL인지에 대한 분석을 하는데 용이한 자료입니다. 해당 자료를 통해 악성 URL이면 분석결과까지 리포팅해서 답변을 해주세요."
        },
        {
            "role" : "user",
            "content" : f"사용자 URL: {url} 결과 : {str(result)}"
        }]
        response = client.responses.create(
            model="gpt-4o",
            input = input,
            tools=[{"type" : "file_search",
                    "vector_store_ids" : [store_id]}]
        )
        return response.output_text

class Agent:
    def __init__(self, client):
        self.client = client
        self.tools = [{
            "type": "function",
            "name": "agent_call",
            "description": "사용자로부터 악성 URL 관련 판단 질문을 받으면 URL 검사와 리포팅을 위해 하위 에이전트를 호출하는 함수입니다.",
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
        self.messages = []
        self.messages.append(
            {"role" : "system",
            "content" : "악성 URL에 대한 질문이 들어오면 Function call을 이용해 사용자의 입력으로부터 URL을 건내주어 응답을 받아야 합니다.\
                Function call에선 하위 에이전트가 URL을 분석해서 당신에게 리포팅을 해줄 것이며 당신은 그 결과를 받고\
                정상이면 그냥 답변하면 되고, 악성이면 하위 에이전트가 리포팅한 정보를 바탕으로 답변해 주세요. 그리고\
                Websearch 툴을 사용하여 대안 사이트 3~4개를 추천해주세요. 이때 사용자의 목적을 알면 목적대로 추천해주고\
                그렇지 않으면 사용자가 처음 보낸 URL의 Domain을 가지고 사용자의 목적을 유추하여 추천해주세요."
            }
        )

    def function_call(self, calls):
        result = []
        for call in calls:
            if call.type != "function_call":
                continue   
            try :
                result.append(call)
                function_args = json.loads(call.arguments)
                output = agent_call(**function_args)
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
        self.messages.extend(result)

    def chat(self, query) : 
        self.messages.append({
            "role": "user",
            "content": query
        })

        # 모델에 응답 요청
        response = self.client.responses.create(
            model="gpt-4o",
            input=self.messages,
            tools=self.tools,
            tool_choice="auto"
        )

        # function_call이 없는 경우, 바로 응답 반환
        if not response or not response.output or all(c.type != "function_call" for c in response.output):
            self.messages.append(
                {"role" : "assistant",
                "content" : response.output_text}
            )
            return response.output_text
        
        # function_call이 있는 경우 처리
        self.function_call(response.output)

        # function_call 결과 포함해서 최종 응답 생성
        final_response = self.client.responses.create(
            model="gpt-4o",
            input=self.messages
        )
        self.messages.append(
            {"role" : "assistant",
             "content" : final_response.output_text}
        )

        return final_response.output_text

if __name__ == "__main__":
    store_id = vector_store_with_file(
        "./악성url관련자료.pdf",
        "knowledge_base",
        client
    )
