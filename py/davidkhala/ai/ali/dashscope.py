from enum import Enum
from http import HTTPStatus

from dashscope import Generation

from davidkhala.ai.model import AbstractClient


class ModelEnum(str, Enum):
    BAILIAN = Generation.Models.bailian_v1
    DOLLY = Generation.Models.dolly_12b_v2
    TURBO= Generation.Models.qwen_turbo
    PLUS = Generation.Models.qwen_plus
    MAX = Generation.Models.qwen_max

class API(AbstractClient):
    """
    Unsupported to use international base_url "https://dashscope-intl.aliyuncs.com"
    """

    model: ModelEnum

    def __init__(self, api_key):
        self.api_key = api_key

    def connect(self):
        ...

    def chat(self, user_prompt: str, **kwargs):

        if not self.messages:
            kwargs['prompt'] = user_prompt
        else:
            kwargs['messages'] = [
                *self.messages,
                {
                    "role": "user",
                    'content': user_prompt
                }
            ]
        # prompt 和 messages 是互斥的参数：如果你使用了 messages，就不要再传 prompt
        responses = Generation.call(
            self.model,
            api_key=self.api_key,
            **kwargs
        )
        if responses.status_code == HTTPStatus.OK:
            return responses.output
        else:
            raise Exception(responses)


