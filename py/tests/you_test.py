import os
import unittest

from davidkhala.ai.agent.you import Client

api_key = os.environ.get('YOU_API_KEY')
class ChatTestCase(unittest.TestCase):

    you = Client(api_key)
    def test_chat(self):
        response = self.you.chat("Teach me how to make an omelet")
        print(response)

class AsyncTestCase(unittest.IsolatedAsyncioTestCase):
    you = Client(api_key)
    async def test_async_chat(self):
        _sum = ''
        async for text in self.you.async_chat("What is a Rain Frog?"):
            _sum += text
        print(_sum)




if __name__ == '__main__':
    unittest.main()

