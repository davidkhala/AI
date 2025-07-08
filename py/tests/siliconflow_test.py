import os
import unittest

from davidkhala.ai.api.siliconflow import SiliconFlow


class APITestCase(unittest.TestCase):
    def test_something(self):
        api_key = os.environ.get('API_KEY')
        model = 'deepseek-ai/DeepSeek-R1-0528-Qwen3-8B'
        _ = SiliconFlow(api_key, model)
        r = _.chat('who am I?')
        print(r)


if __name__ == '__main__':
    unittest.main()
