import os
from unittest import skipIf, TestCase
from davidkhala.ai.openai.native import NativeClient



class CITestCase(TestCase):
    def setUp(self):
        self.api_key = os.getenv("API_KEY")
        self.client = NativeClient(api_key=self.api_key)
    def test_connect(self):
        print(self.client.models)
        
        
