from abc import ABC
from openai import OpenAI

class OpenApi(ABC):
    def __init__(self, model, api_key, base_url):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.client = self.get_client()

    def get_client(self):
        return OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def get_result(self, messages):
        # 调用大模型
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
            reasoning_effort="high",
            extra_body={"thinking": {"type": "enabled"}}
        )

        return response
        # return response.choices[0].message.content

OpenApi = OpenApi


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    load_dotenv()
    model = os.getenv("ALI_MODEL")
    base_url = os.getenv("ALI_BASE_URL")
    api_key = os.getenv("DASHSCOPE_API_KEY")
    print(OpenApi(model=model,base_url=base_url,api_key=api_key).get_client())









