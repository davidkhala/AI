import os
import unittest

from davidkhala.ai.api.open import OpenRouter


class APITestCase(unittest.TestCase):
    def test_prompt(self):
        api_key = os.environ.get('API_KEY')
        openrouter = OpenRouter(api_key)
        r = openrouter.chat('who am I?')
        print(r)


if __name__ == "__main__":
    unittest.main()
