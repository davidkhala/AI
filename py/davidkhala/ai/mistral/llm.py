from davidkhala.llm.model.chat import ChoicesChat, on_response
from davidkhala.llm.model.embed import EmbeddingAware
from davidkhala.llm.model.garden import GardenAlike
from davidkhala.utils.protocol import ID
from mistralai import ResponseFormat

from davidkhala.ai.mistral import Client as MistralClient


class Client(ChoicesChat, EmbeddingAware, MistralClient, GardenAlike):
    def __init__(self, api_key: str):
        super().__init__(api_key=api_key)

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

    def list_models(self) -> list[ID]:
        return self.client.models.list().data
