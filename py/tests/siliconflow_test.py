import os
import time
import unittest

from davidkhala.ai.api.siliconflow import SiliconFlow
from requests import HTTPError

api_key = os.environ.get('API_KEY')
_ = SiliconFlow(api_key)

class CommonTests(unittest.TestCase):
    def test_models(self):
        _models = _.list_models()
        print(_models)
class ChatTestCase(unittest.TestCase):

    def test_chat(self):
        _.as_chat('deepseek-ai/DeepSeek-R1-0528-Qwen3-8B')
        r = _.chat('who am I?')
        print(r)
class EmbeddingTestCase(unittest.TestCase):
    def test_array(self):
        _.as_embeddings('BAAI/bge-m3')
        start_time = time.time()
        r = _.encode("abc--------------------------------", "edf-----------------")
        print(time.time() - start_time)
        self.assertEqual(2, len(r))
    def test_empty(self):
        _.as_embeddings('BAAI/bge-m3')
        with self.assertRaises(HTTPError) as e:
            r = _.encode("")
        self.assertEqual(400, e.exception.response.status_code )



if __name__ == '__main__':
    unittest.main()
