import os
import unittest

from davidkhala.ai.openai import OpenAIClient


class OpenAITestCase(unittest.TestCase):
    def test_connect(self):
        client = OpenAIClient(os.environ.get("API_KEY"))
        client.as_azure(os.environ.get("PROJECT"))
        client.connect()

if __name__ == '__main__':
    unittest.main()
