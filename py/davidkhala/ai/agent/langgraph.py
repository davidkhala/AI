from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent


class Agent:

    def __init__(self, model, instruction, *tools):
        self.agent = create_react_agent(
            model=model,
            tools=tools,
            prompt=instruction
        )
    def invoke(self, content):
        return self.agent.invoke({"messages": [{"role": "user", "content": content}]})['messages'][-1]

class OpenRouterModel:
    def __init__(self, api_key):
        self.api_key = api_key

    def init_chat_model(self, model):
        return init_chat_model(
            base_url='https://openrouter.ai/api/v1',
            model=model,model_provider= "openai",
            configurable_fields = ['api_key'],
            api_key = self.api_key
        )
