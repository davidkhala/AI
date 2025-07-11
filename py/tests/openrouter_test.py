import os
import unittest

from davidkhala.ai.api.open import OpenRouter


class APITestCase(unittest.TestCase):
    api_key = os.environ.get('API_KEY')
    openrouter = OpenRouter(api_key)

    def test_chat(self):
        r = self.openrouter.chat('who am I?')
        print(r)

    def test_models(self):
        models = self.openrouter.free_models
        self.assertEqual(52, len(models))


if __name__ == "__main__":
    unittest.main()
