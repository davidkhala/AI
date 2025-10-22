import datetime
from abc import abstractmethod
from typing import List

from davidkhala.utils.http_request import Request

from davidkhala.ai.model import AbstractClient


class API(AbstractClient, Request):
    def __init__(self, api_key: str, base_url: str):
        super().__init__({
            "bearer": api_key
        })
        self.base_url = base_url + '/v1'

    @property
    @abstractmethod
    def free_models(self) -> list[str]:
        ...

    def chat(self, *user_prompt: str, **kwargs):
        messages = [
            *self.messages,
            *[{
                "role": "user",
                "content": _
            } for _ in user_prompt],
        ]

        json = {
            "messages": messages,
            **kwargs,
        }

        response = self.request(f"{self.base_url}/chat/completions", "POST", json=json)

        return {
            "data": list(map(lambda x: x['message']['content'], response['choices'])),
            "meta": {
                "usage": response['usage'],
                "created": datetime.datetime.fromtimestamp(response['created'])
            },
            'model': response['model'],
        }

    def list_models(self):
        response = self.request(f"{self.base_url}/models", "GET")
        return response['data']


    def encode(self, *_input: str) -> List[List[float]]:
        """
        TODO from siliconflow only
        :param _input:
        :return:
        """
        json = {
            'input'
        }
        response =self.request(f"{self.base_url}/embeddings", "POST", json=json)
        return [ _['embedding'] for _ in response['data']]