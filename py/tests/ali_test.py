import os
import unittest

from davidkhala.ai.ali.dashscope import API, ModelEnum

api_key = os.environ.get('API_KEY')


class DashscopeTestCase(unittest.TestCase):
    api = API(api_key)
    prompt = '今天天气好吗？'

    def test_chat(self):
        self.api.as_chat(ModelEnum.PLUS)
        r = self.api.chat(self.prompt)
        print(r)

    def test_conversation(self):
        self.api.as_chat(ModelEnum.MAX,
                         "你是一位专业翻译官，负责将接下来用户提供的中学学校名称翻译，并精准匹配到其官方的中文校名。用户输入的所有整体就是一个待翻译校名，。你也只回答翻译后的校名")
        r = self.api.chat('Chiway Repton High School Xiamen',
            enable_search=True,
        )

        self.assertNotEqual('厦门华锐莱普顿学校', r['text'])

    def test_embed(self):
        self.api.as_embeddings()
        r = self.api.encode(self.prompt)
        print(r)


if __name__ == '__main__':
    unittest.main()
