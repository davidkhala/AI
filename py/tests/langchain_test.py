import os
import unittest

from langchain_core.messages import AIMessage

from davidkhala.ai.agent.langgraph import Agent, OpenRouterModel

api_key = os.environ.get('API_KEY')


class GetStartedTestCase(unittest.TestCase):

    def test_invoke(self):
        """https://langchain-ai.github.io/langgraph/#get-started"""

        def get_weather(city: str) -> str:
            """Get weather for a given city."""
            return f"It's always sunny in {city}!"

        model = OpenRouterModel(api_key).init_chat_model("deepseek/deepseek-chat-v3.1:free")
        agent = Agent(
            model,
            "You are a helpful assistant",
            get_weather
        )
        r: AIMessage = agent.invoke("what is the weather in Hongkong")
        print(r.content)


class ModelTestCase(unittest.TestCase):
    def test_openrouter(self):
        model = OpenRouterModel(api_key).init_chat_model("deepseek/deepseek-chat-v3.1:free")
        r: AIMessage = model.invoke("what is the weather in sf")
        print(r.content)


if __name__ == '__main__':
    unittest.main()
