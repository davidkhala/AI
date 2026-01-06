from typing import AsyncIterator

from youdotcom import You, models
from youdotcom.types.typesafe_models import (
    AgentType,
    stream_text_tokens
)
from youdotcom.utils import eventstreaming

from davidkhala.ai.model import AbstractClient


class Client(AbstractClient):
    def __init__(self, api_key: str):
        self.client = You(api_key_auth=api_key)

    def chat(self, user_prompt: str) -> str:
        res = self.client.agents.runs.create(
            agent=AgentType.EXPRESS,
            input=user_prompt,
            stream=True,
        )

        return stream_text_tokens(res)

    async def async_chat(self, user_prompt: str) -> AsyncIterator[str]:
        res: eventstreaming.EventStreamAsync[models.Data] = await self.client.agents.runs.create_async(
            agent=AgentType.EXPRESS,
            input=user_prompt,
            stream=True,
        )

        async for event in res:
            if event.type == 'response.output_text.delta':
                yield event.response.delta

    def __enter__(self):
        self.client.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
