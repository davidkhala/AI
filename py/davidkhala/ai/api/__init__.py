import datetime
from abc import abstractmethod, ABC

import requests


class API(ABC):
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.model = None

    @property
    @abstractmethod
    def free_models(self)->list[str]:
        ...

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
        # timeout=50 to cater siliconflow
        response = requests.post(f"{self.base_url}/v1/chat/completions", headers=headers, json=json, timeout=50)
        parsed_response = response.json()


        match parsed_response:
            case dict():
                err = parsed_response.get('error')
                if err is not None:
                    raise Exception(err)
            case str():
                raise Exception(parsed_response)
        return {
            "data": list(map(lambda x: x['message']['content'], parsed_response['choices'])),
            "meta": {
                "usage": parsed_response['usage'],
                "created": datetime.datetime.fromtimestamp(parsed_response['created'])
            }
        }
