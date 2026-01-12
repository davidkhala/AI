import unittest
from davidkhala.ai.mistral import Client
import os
class ChatTest(unittest.TestCase):

    def setUp(self):
        api_key = os.environ.get("API_KEY")
        self.client = Client(api_key)
    def test_chat(self):
        message = "Who is the best French painter? Answer in one short sentence."
        print(self.client.chat(message))


if __name__ == "__main__":
    unittest.main()