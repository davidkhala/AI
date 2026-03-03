from typing import AsyncIterator

from youdotcom import You, models
from youdotcom.models import Web, ExpressAgentRunsRequest, AdvancedAgentRunsRequest, AgentRunsBatchResponse, \
    ContentsFormats, AgentsRunsRequest, AgentRunsStreamingResponse
from youdotcom.utils import eventstreaming


class Client:
    def __init__(self, api_key: str):
        self.client = You(api_key_auth=api_key)

    @staticmethod
    def build_request(user_prompt: str,
                      tools: list[models.Tool] = None) -> ExpressAgentRunsRequest | AdvancedAgentRunsRequest:
        if tools and len(tools) > 1:
            req = AdvancedAgentRunsRequest(
                input=user_prompt,
                tools=tools,
            )
        else:
            req = ExpressAgentRunsRequest(
                input=user_prompt,
                tools=tools,
            )
        return req

    def chat(self, user_prompt: str, *, tools: list[models.Tool] = None) -> str:
        req = Client.build_request(user_prompt, tools)
        req.stream = False
        res: AgentRunsBatchResponse = self.client.agents.runs.create(
            request=req,
        )
        lines = [_.text for _ in res.output if _.type == 'message.answer']
        return "".join(lines)

    def scrape(self, *urls: str) -> list[str]:
        """
        :return: the content of the web pages as Markdown format (incl. metadata)
        """
        res = self.client.contents.generate(
            urls=list(urls),
            formats=[ContentsFormats.MARKDOWN],
        )
        return [_.markdown for _ in res]

    def search(self, query: str) -> list[Web]:
        res = self.client.search.unified(
            query=query
        )
        return res.results.web

    async def async_chat(self, user_prompt: str, *, tools: list[models.Tool] = None) -> AsyncIterator[str]:
        req = Client.build_request(user_prompt, tools)
        req.stream = True
        res: eventstreaming.EventStreamAsync[AgentRunsStreamingResponse] = await self.client.agents.runs.create_async(
            request=req,
        )

        async for _ in res:
            if _.event == 'response.output_text.delta':
                yield _.data.response.delta

    def __enter__(self):
        self.client.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
