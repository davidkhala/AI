from typing import AsyncIterator

from youdotcom import You, models
from youdotcom.models import Web
from youdotcom.types.typesafe_models import AgentType, get_text_tokens, Format
from youdotcom.utils import eventstreaming


class Client:
    def __init__(self, api_key: str):
        self.client = You(api_key_auth=api_key)

    def chat(self, user_prompt: str, *, tools: list[models.Tool] = None) -> str:
        res = self.client.agents.runs.create(
            agent=AgentType.ADVANCED if tools else AgentType.EXPRESS,
            input=user_prompt,
            stream=False,
            tools=tools,
        )

        return "".join(get_text_tokens(res))

    def scrape(self, *urls: str) -> list[str]:
        """
        :return: the content of the web pages as Markdown format (incl. metadata)
        """
        res = self.client.contents.generate(
            urls=list(urls),
            format_=Format.MARKDOWN,
        )
        return [_.markdown for _ in res]

    def search(self, query: str) -> list[Web]:
        res = self.client.search.unified(
            query=query
        )
        return res.results.web

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
