from typing import Literal

from httpx import URL
from openai import OpenAI

from davidkhala.ai.model import AbstractClient
from davidkhala.ai.model.chat import on_response


class Client(AbstractClient):
    def __init__(self, client: OpenAI):
        super().__init__()
        self.client:OpenAI = client
        self.base_url:URL = client.base_url
        self.api_key = client.api_key
        self.encoding_format:Literal["float", "base64"] = "float"
        self.n:int = 1
    def connect(self):
        try:
            type(self).models.fget(self)
            return True
        except:  # TODO make specific
            return False

    @property
    def models(self):
        return self.client.models.list()

    def encode(self, *_input: str) -> list[list[float]]:
        response = self.client.embeddings.create(
            model=self.model,
            input=list(_input),
            encoding_format=self.encoding_format
        )
        return [item.embedding for item in response.data]

    def chat(self, *user_prompt, **kwargs):

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages_from(*user_prompt),
            n=self.n,
            **kwargs
        )

        return on_response(response, self.n)

    def close(self):
        self.client.close()



