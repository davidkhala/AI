import os
import unittest

from davidkhala.ai.api.openrouter import OpenRouter


class APITestCase(unittest.TestCase):
    api_key = os.environ.get('API_KEY')
    openrouter = OpenRouter(api_key)

    def test_chat(self):
        self.openrouter.as_chat("deepseek/deepseek-chat-v3.1:free")
        r = self.openrouter.chat('who am I?')
        print(r)
        self.assertTrue(type(r['data'])==list)
        self.assertEqual(1, len(r['data']))
    def test_chat_models(self):
        self.openrouter.models = ["deepseek/deepseek-chat-v3.1:free", "deepseek/deepseek-chat-v3.1"]
        r = self.openrouter.chat('who am I?')
        print(r) # only has one answer. Openrouter use models as pool for load-balance only
        self.assertEqual("deepseek/deepseek-chat-v3.1:free", r['model'])
    def test_models(self):
        models = self.openrouter.free_models
        self.assertGreaterEqual(len(models), 51)
        print(models)


if __name__ == "__main__":
    unittest.main()
