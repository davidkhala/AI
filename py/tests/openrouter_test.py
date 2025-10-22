import os
import unittest

from davidkhala.ai.api.openrouter import OpenRouter
from requests import HTTPError


class APITestCase(unittest.TestCase):

    def setUp(self):
        self.api_key = os.environ.get('API_KEY')
        self.openrouter = OpenRouter(self.api_key)

    def test_chat(self):
        self.openrouter.as_chat("deepseek/deepseek-chat-v3.1:free")
        r = self.openrouter.chat('who am I?')
        self.assertTrue(type(r['data']) == list)
        self.assertEqual(1, len(r['data']))

    def test_chat_models(self):
        self.openrouter.models = ["deepseek/deepseek-chat-v3.1:free", "deepseek/deepseek-chat-v3.1"]
        r = self.openrouter.chat('who am I?')
        print(r)  # only has one answer. Openrouter use models as pool for load-balance only
        self.assertEqual("deepseek/deepseek-chat-v3.1:free", r['model'])

    def test_models(self):
        models = self.openrouter.free_models
        self.assertGreaterEqual(len(models), 51)
        print(models)

    def test_google_limit(self):
        for model in ['google/gemma-3n-e2b-it:free']:
            self.openrouter.as_chat(model)
            with self.assertRaises(HTTPError) as e:
                self.openrouter.chat('-')
            self.assertEqual(e.exception.response.status_code, 400)
    def test_google(self):
        self.openrouter.as_chat('google/gemini-2.5-flash-lite-preview-09-2025')
        r = self.openrouter.chat('-')
        print(r)

    def test_openai(self):
        allowed_models = ['openai/gpt-oss-20b:free', 'openai/gpt-5-nano']
        for model in allowed_models:
            self.openrouter.as_chat(model)
            r = self.openrouter.chat('return True')
            print(model, r['data'][0])
    def test_openai_limit(self):
        self.openrouter.as_chat('openai/gpt-4.1-nano')
        with self.assertRaises(HTTPError) as e:
            self.openrouter.chat('-')
        self.assertEqual(e.exception.response.status_code, 403)


if __name__ == "__main__":
    unittest.main()
