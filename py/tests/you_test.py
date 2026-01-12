import os
import unittest
from unittest import skipIf

from youdotcom.models import ComputeTool, ResearchTool
from youdotcom.types.typesafe_models import SearchEffort, Verbosity

from davidkhala.ai.agent.you import Client

api_key = os.environ.get('API_KEY')


class ChatTestCase(unittest.TestCase):
    you = Client(api_key)

    def test_chat(self):
        response = self.you.chat("Teach me how to make an omelet")
        print(response)

    @skipIf(os.environ.get('CI'), "Research cost $15 / request")
    def test_agent(self):
        response = self.you.chat(
            "Research and calculate the latest trends and the square root of 169. Show your work.",
            tools=[
                ComputeTool(),
                ResearchTool(
                    search_effort=SearchEffort.AUTO,
                    report_verbosity=Verbosity.HIGH,
                ),
            ]
        )
        print(response)

    def test_scrape(self):
        for content in self.you.scrape("https://thei.edu.hk"):
            print(content)

    def test_search(self):
        for web in self.you.search('latest AI developments'):
            print(web)


class AsyncTestCase(unittest.IsolatedAsyncioTestCase):
    you = Client(api_key)

    async def test_async_chat(self):
        _sum = ''
        async for text in self.you.async_chat("What is a Rain Frog?"):
            _sum += text
        print(_sum)


if __name__ == '__main__':
    unittest.main()
