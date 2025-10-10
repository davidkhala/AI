import os
import unittest

from davidkhala.ai.api.openrouter import OpenRouter


class APITestCase(unittest.TestCase):
    api_key = os.environ.get('API_KEY')
    openrouter = OpenRouter(api_key, "deepseek/deepseek-chat-v3.1:free")

    def test_chat(self):
        r = self.openrouter.chat('who am I?')
        print(r)
        self.assertTrue(type(r['data'])==list)
        self.assertEqual(1, len(r['data']))
    def test_models(self):
        models = self.openrouter.free_models
        self.assertGreaterEqual(len(models), 51)
        print(models)


if __name__ == "__main__":
    unittest.main()
