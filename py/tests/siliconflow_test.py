import os
import unittest

from davidkhala.ai.api.siliconflow import SiliconFlow


class APITestCase(unittest.TestCase):
    api_key = os.environ.get('API_KEY')
    _ = SiliconFlow(api_key)

    def test_chat(self):
        self._.as_chat('deepseek-ai/DeepSeek-R1-0528-Qwen3-8B')

        r = self._.chat('who am I?')
        print(r)

    def test_models(self):
        _models = self._.list_models()
        print(_models)


if __name__ == '__main__':
    unittest.main()
