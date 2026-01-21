# https://github.com/mistralai/client-python

from mistralai import ResponseFormat

from davidkhala.ai.mistral import Client as MistralClient
from davidkhala.ai.model import AbstractClient as AIAware
from davidkhala.ai.model.chat import on_response


class Client(AIAware, MistralClient):
    def __init__(self, api_key: str):
        AIAware.__init__(self)
        MistralClient.__init__(self, api_key)
        self.n = 1

    def as_chat(self, model="mistral-large-latest", sys_prompt: str = None):
        super().as_chat(model, sys_prompt)

    def as_embeddings(self, model="mistral-embed"):
        super().as_embeddings(model)

    def chat(self, *user_prompt, **kwargs):
        response = self.client.chat.complete(
            model=self.model,
            messages=self.messages_from(*user_prompt), stream=False, response_format=ResponseFormat(type='text'),
            n=self.n,
        )

        return on_response(response, self.n)

    def encode(self, *_input: str) -> list[list[float]]:
        res = self.client.embeddings.create(
            model=self.model,
            inputs=_input,
        )
        return [d.embedding for d in res.data]

    @property
    def models(self) -> list[str]:
        return [_.id for _ in self.client.models.list().data]
