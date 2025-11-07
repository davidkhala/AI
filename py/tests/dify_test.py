import os
import unittest
from davidkhala.ai.agent.dify.knowledge import Dataset, Document
from davidkhala.utils.syntax.path import resolve


class DatasetTest(unittest.TestCase):
    api_key = os.getenv('API_KEY')
    client = Dataset(api_key)

    def test_list(self):
        for _id in self.client.ids:
            print(_id)

    def test_get(self):
        id = '733e7159-2963-462d-b839-9c54d5f33a7e'
        instance = Dataset.Instance(self.client, id)
        print(instance.get())


class DocumentTest(unittest.TestCase):
    def setUp(self):
        id = '733e7159-2963-462d-b839-9c54d5f33a7e'
        self.client = Dataset.Instance(DatasetTest.client, id)
    def test_upload(self):
        r = self.client.upload(None, path=resolve(__file__, "../../README.md"))
        print(r)
        url = 'https://raw.githubusercontent.com/davidkhala/AI/refs/heads/main/py/README.md'
        r = self.client.upload(None, url=url)
        print(r)
        doc_id = r['id']
        r = self.client.upload(None, url=url,document_id=doc_id)
        print(r)
    def test_list(self):
        for documents in self.client.list_documents():
            for doc in documents:
                print(doc)
                print(doc['name'])
    def test_has(self):
        name = 'Admission - Technological and Higher Education Institute of Hong Kong.html'
        self.assertTrue(self.client.has_document(name))
        self.assertFalse(self.client.has_document('README'))

    def test_exist(self):
        doc_id= '26cc41ea-14a1-425d-934a-f68cb258a91e'
        doc = Document(self.client, doc_id)
        self.assertTrue(doc.exist())
        doc_id = '26cc41ea-14a1-425d-934a-f68cb258a91e'+'1'
        doc = Document(self.client, doc_id)
        self.assertFalse(doc.exist())


if __name__ == '__main__':
    unittest.main()
