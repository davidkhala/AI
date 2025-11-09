import os
import unittest

from davidkhala.utils.syntax.path import resolve
from requests import HTTPError

from davidkhala.ai.agent.dify import with_datetime
from davidkhala.ai.agent.dify.knowledge import Dataset, Document


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
        dataset_id = '733e7159-2963-462d-b839-9c54d5f33a7e'
        self.client = Dataset.Instance(DatasetTest.client, dataset_id)

    def test_upload_readme(self):
        r = self.client.upload(None, path=resolve(__file__, "../../README.md"))
        print(r)
        url = 'https://raw.githubusercontent.com/davidkhala/AI/refs/heads/main/py/README.md'
        r = self.client.upload(None, url=url)
        print(r)
        # update will be 400
        # doc_id = r['id']
        # r = self.client.upload(None, url=url,document_id=doc_id)
        # print(r)
        composite_file = with_datetime("README.md")
        r = self.client.upload(composite_file, url=url)
    def test_upload_pdf(self):
        pdf_path = resolve(__file__, '../fixtures/empty.pdf')
        self.client.upload(None, path=pdf_path)
    def test_update(self):
        ... # FIXME cannot rename
        # TODO try update content of README.md


    def test_unsupported_upload(self):
        # png is not supported
        img_url = 'https://media.goodschool.hk/images/ulogo/thei.png'
        with self.assertRaises(HTTPError) as context:
            self.client.upload(None, url=img_url)
        self.assertEqual(context.exception.response.status_code, 400)
        # html should be supported
        html_path = resolve(__file__,
                            "../fixtures/About THEi - Technological and Higher Education Institute of Hong Kong.html")
        with self.assertRaises(HTTPError) as context:
            self.client.upload(None, path=html_path)
        self.assertEqual(context.exception.response.status_code, 403)

    def test_list(self):
        for documents in self.client.list_documents():
            for doc in documents:
                # doc has content, can be length
                print(doc['name'])

    def test_has(self):
        name = 'Admission - Technological and Higher Education Institute of Hong Kong.html'
        self.assertTrue(self.client.has_document(name))
        self.assertFalse(self.client.has_document('README'))

    def test_exist(self):
        doc_id = '26cc41ea-14a1-425d-934a-f68cb258a91e' + '1'
        doc = Document(self.client, doc_id)
        self.assertFalse(doc.exist())
        doc_id = '26cc41ea-14a1-425d-934a-f68cb258a91e'
        doc = Document(self.client, doc_id)
        self.assertTrue(doc.exist())
        print(doc.get())


if __name__ == '__main__':
    unittest.main()
