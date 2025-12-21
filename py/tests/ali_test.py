import os
import unittest

from agentbay.browser import BrowserOption

from davidkhala.ai.ali.dashscope import API, ModelEnum
from davidkhala.ai.ali.agentbay import Client as BayClient
from playwright.sync_api import sync_playwright


class DashscopeTestCase(unittest.TestCase):
    prompt = '今天天气好吗？'

    def setUp(self):
        api_key = os.environ.get('API_KEY')
        self.api = API(api_key)

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


class AgentBayTestCase(unittest.TestCase):

    def setUp(self):
        api_key = os.getenv("AGENTBAY_API_KEY")
        self.agent = BayClient(api_key)
        assert self.agent.open()

    def test_AIBrowser(self):
        self.agent.session.browser.initialize(BrowserOption())
        url = self.agent.session.browser.get_endpoint_url()
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(url)
            page = browser.new_page()
            page.goto("https://www.aliyun.com")
            self.assertEqual('Captcha Interception', page.title())
            browser.close()

    def tearDown(self):
        self.agent.close()


if __name__ == '__main__':
    unittest.main()
