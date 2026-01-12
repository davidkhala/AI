# https://github.com/mistralai/client-python

from davidkhala.ai.model import AbstractClient
from mistralai import Mistral, ChatCompletionResponse, ResponseFormat
from davidkhala.ai.model.chat import on_response

class Client(AbstractClient):
    n = 1

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = Mistral(api_key=api_key)
        self.model = "mistral-large-latest"
        self.messages = []

    def __enter__(self):
        self.client.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.client.__exit__(exc_type, exc_val, exc_tb)

    def chat(self, *user_prompt, **kwargs):
        response: ChatCompletionResponse = self.client.chat.complete(
            model=self.model,
            messages=[
                *self.messages,
                *[{"content": m, "role": "user"} for m in user_prompt]
            ], stream=False, response_format=ResponseFormat(type='text'),
            n=self.n,
        )

        return on_response(response, self.n)
