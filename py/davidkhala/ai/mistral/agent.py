from typing import Literal, Union

from mistralai import Agent, ToolExecutionEntry, FunctionCallEntry, MessageOutputEntry, AgentHandoffEntry

from davidkhala.ai.mistral import Client as MistralClient
from davidkhala.ai.model.chat import messages_from


class Agents(MistralClient):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.instructions: str | None = None
        self.model = None

    def as_chat(self, model="mistral-large-latest", sys_prompt: str = None):
        self.model = model
        if sys_prompt is not None:
            self.instructions = sys_prompt

    def create(self, name,
               *,
               web_search: Literal["web_search", "web_search_premium"] = None
               ) -> Agent:
        """
        :param name:
        :param web_search:
            "web_search_premium": beyond search engine, add news provider as source
        :return:
        """
        tools = []
        if web_search:
            tools.append({"type": web_search})
        agent = self.client.beta.agents.create(
            model=self.model,
            name=name,
            tools=tools,
            instructions=self.instructions
        )
        return agent

    def chat(self, agent_id: str, *user_prompt: str) -> tuple[
        list[Union[ToolExecutionEntry, FunctionCallEntry, MessageOutputEntry, AgentHandoffEntry]],
        str
    ]:
        response = self.client.beta.conversations.start(
            agent_id=agent_id,
            inputs=messages_from(*user_prompt)
        )

        return response.outputs, response.conversation_id
