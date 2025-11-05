import unittest
from davidkhala.ai.agent.ragflow import Client

class ClientTest(unittest.TestCase):
    def setUp(self):
        self.client = Client("ragflow")
        print(self.client.datasets)
    def test_datasets(self):
        pass

if __name__ == "__main__":
    unittest.main()