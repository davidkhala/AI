import os
import unittest

from davidkhala.ai.api.siliconflow import SiliconFlow


api_key = os.environ.get('API_KEY')
_ = SiliconFlow(api_key)

class CommonTests(unittest.TestCase):
    def test_models(self):
        _models = _.list_models()
        print(_models)
class ChatTestCase(unittest.TestCase):

    def test_chat(self):
        _.as_chat('deepseek-ai/DeepSeek-R1-0528-Qwen3-8B')
        r = _.chat('who am I?')
        print(r)
class EmbeddingTestCase(unittest.TestCase):
    ...



if __name__ == '__main__':
    unittest.main()
