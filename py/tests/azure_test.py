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
    def test_connect(self):

        key = os.environ.get("DEPLOYMENT_KEY")
        deployment = os.environ.get("DEPLOYMENT")
        model  = os.environ.get("DEPLOYMENT_MODEL")
        client = ModelDeploymentClient(
            key,
            deployment,
        )
        client.connect()
        client.as_chat(model, "You are a helpful assistant.")

        response = client.chat("Don't reply me anything now.")

        print(response)


if __name__ == '__main__':
    unittest.main()
