import os
import unittest

from davidkhala.ai.openai.azure import ModelDeploymentClient, OpenAIClient


class OpenAITestCase(unittest.TestCase):
    def setUp(self):
        api_key = os.environ.get("API_KEY")
        project = os.environ.get("PROJECT")
        self.client = OpenAIClient(api_key, project)

    def test_connect(self):
        self.client.connect()

    def test_chat(self):
        self.client.as_chat()
        print(self.client.chat("hello"))


class ModelDeploymentTestCase(unittest.TestCase):
    def setUp(self):
        key = os.environ.get("DEPLOYMENT_KEY")
        deployment = os.environ.get("DEPLOYMENT")
        self.client = ModelDeploymentClient(key, deployment)

    def test_connect(self):
        self.client.connect()

    def test_chat(self):
        self.client.as_chat("gpt-4o", "You are a helpful assistant.")
        response = self.client.chat("Don't reply me anything now.", "What is your model name?")
        self.assertEqual(1, len(response))
        print(response[0])

    def test_embedding(self):
        self.client.as_embeddings("text-embedding-3-large")
        print(self.client.encode("Attention is all you need"))


if __name__ == '__main__':
    unittest.main()
