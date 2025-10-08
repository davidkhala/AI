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

        free_model = "mistralai/mistral-small-3.2-24b-instruct:free" # chosen by https://openrouter.ai/models?supported_parameters=tools&max_price=0
        model = OpenRouterModel(api_key).init_chat_model(free_model)
        agent = Agent(
            model,
            "You are a helpful assistant",
            get_weather
        )
        r = agent.invoke("what is the weather in Hongkong")

        print(r) # TODO no actual response found


class ModelTestCase(unittest.TestCase):
    def test_openrouter(self):
        model = OpenRouterModel(api_key).init_chat_model("openai/gpt-oss-20b:free")
        r: AIMessage = model.invoke("what is the weather in sf")
        print(r.content)


if __name__ == '__main__':
    unittest.main()
