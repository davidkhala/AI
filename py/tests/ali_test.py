import os
import unittest

from davidkhala.ai.ali.dashscope import API, ModelEnum


class DashscopeTestCase(unittest.TestCase):
    def test_connect(self):
        prompt = '今天天气好吗？'
        api_key = os.environ.get('API_KEY')
        api = API(api_key)

        api.as_chat(ModelEnum.PLUS)
        r = api.chat(prompt)
        print(r)



if __name__ == '__main__':
    unittest.main()
