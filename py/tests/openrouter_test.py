import os
import unittest
from davidkhala.ai.router.open import OpenRouter


class APITestCase(unittest.TestCase):
    def test_prompt(self):
        api_key = os.environ.get('API_KEY')
        openrouter = OpenRouter(api_key)
        r = openrouter.post('who am I?')
        print(r)


if __name__ == "__main__":
    unittest.main()
