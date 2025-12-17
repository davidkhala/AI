import os
import unittest

from davidkhala.ai.openrouter import Client as OpenRouterClient, Admin


class SDKTestCase(unittest.TestCase):
    def setUp(self):
        api_key = os.environ.get('API_KEY')
        admin_key = os.environ.get('PROVISIONING_API_KEY')
        self.openrouter = OpenRouterClient(api_key)
        self.admin = Admin(admin_key)

    def test_connect(self):
        self.assertTrue(self.openrouter.connect())
    def test_keys(self):
        print(self.admin.keys)

    def test_chat(self):
        self.openrouter.as_chat('minimax/minimax-m2')
        r = self.openrouter.chat('Hello!')
        print(r)


if __name__ == "__main__":
    unittest.main()
