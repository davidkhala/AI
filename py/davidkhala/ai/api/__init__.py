import datetime
from abc import abstractmethod

import requests

from davidkhala.ai.model import AbstractClient


class API(AbstractClient):
    def __init__(self, api_key: str, base_url: str):
        self.base_url = base_url+'/v1'
        self.headers = {
            "Authorization": f"Bearer {api_key}",
        }

    @property
    @abstractmethod
    def free_models(self)->list[str]:
        ...

    def chat(self, *user_prompt: str, **kwargs):

        messages = [
            *self.messages,
            * [{
                "role": "user",
                "content": _
            } for _ in user_prompt],
        ]

        json = {
            "messages": messages,
            **kwargs,
        }

        # timeout=50 to cater siliconflow
        response = requests.post(f"{self.base_url}/chat/completions", headers=self.headers, json=json, timeout=50)
        parsed_response = API.parse(response)


        return {
            "data": list(map(lambda x: x['message']['content'], parsed_response['choices'])),
            "meta": {
                "usage": parsed_response['usage'],
                "created": datetime.datetime.fromtimestamp(parsed_response['created'])
            }
        }
    @staticmethod
    def parse(response):
        parsed_response = response.json()

        match parsed_response:
            case dict():
                err = parsed_response.get('error')
                if err is not None:
                    raise Exception(err)
            case str():
                raise Exception(parsed_response)
        return parsed_response
    def list_models(self):
        response = requests.get(f"{self.base_url}/models", headers=self.headers)
        return API.parse(response)['data']