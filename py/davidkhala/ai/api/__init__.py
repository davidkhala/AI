import datetime
from abc import abstractmethod, ABC

import requests


class API(ABC):
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.model = None

    @abstractmethod
    def pre_request(self, headers: dict, data: dict):
        data["model"] = self.model



    def chat(self, prompt, system_prompt: str = None):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        if system_prompt is not None:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        json = {
            "messages": messages
        }
        self.pre_request(headers, json)

        response = requests.post(f"{self.base_url}/v1/chat/completions", headers=headers, json=json).json()
        err = response.get('error')
        if err is not None:
            raise Exception(err)


        return {
            "data": list(map(lambda x: x['message']['content'], response['choices'])),
            "meta": {
                "provider": response["provider"],
                "usage": response['usage'],
                "created": datetime.datetime.fromtimestamp(response['created'])
            }
        }
