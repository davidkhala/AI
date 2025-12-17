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
            _.encode("")
        self.assertEqual(400, e.exception.response.status_code)


class RerankTestCase(unittest.TestCase):

    def test_model_compare(self):
        _.model = 'BAAI/bge-reranker-v2-m3'
        query = 'apple'
        docs = ["apple", "banana", "fruit", "vegetable"]
        self.assertEqual('apple', _.which(query, docs)[0])
        _.model = 'Qwen/Qwen3-Reranker-8B'  # unnatural model, and inconsistent
        self.assertIn(_.which(query, docs)[0], ['apple', 'banana'])
        _.model = 'Qwen/Qwen3-Reranker-4B' # unnatural model, and inconsistent
        self.assertIn(_.which(query, docs)[0], ['banana', 'fruit'])
        _.model = 'Qwen/Qwen3-Reranker-0.6B'
        self.assertEqual('apple', _.which(query, docs)[0])

    def test_null(self):
        _.model = 'BAAI/bge-reranker-v2-m3'
        with self.assertRaises(HTTPError) as e:
            _.which('apple', [])  # bad request
        self.assertEqual(400, e.exception.response.status_code)


if __name__ == '__main__':
    unittest.main()
