import os
import unittest
from davidkhala.ai.agent.dify.knowledge import Dataset


class DatasetTest(unittest.TestCase):
    api_key = os.getenv('API_KEY')
    def setUp(self):
        self.client = Dataset(self.api_key)
    def test_list(self):
        for sub_list in  self.client.list_all():
            print(sub_list)

if __name__ == '__main__':
    unittest.main()