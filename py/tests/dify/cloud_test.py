
import os
import unittest
from datetime import datetime

from davidkhala.utils.syntax.path import resolve
from requests import HTTPError

from davidkhala.ai.agent.dify.api.app import Feedbacks, Conversation
from davidkhala.ai.agent.dify.api.knowledge import Dataset, Document, Chunk


class CloudTest(unittest.TestCase):
    def setUp(self):
        self.api_key = os.getenv('KB_API_KEY')


class DatasetTest(CloudTest):

    def setUp(self):
        super().setUp()
        self.client = Dataset(self.api_key)

    def test_list(self):
        for _id in self.client.ids:
            print(_id)

    def test_get(self):
        id = '733e7159-2963-462d-b839-9c54d5f33a7e'
        instance = Dataset.Instance(self.client, id)
        print(instance.get())


class DocumentTest(CloudTest):
    def setUp(self):
        super().setUp()
        dataset_id = '733e7159-2963-462d-b839-9c54d5f33a7e'
        self.client = Dataset.Instance(Dataset(self.api_key), dataset_id)

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

        composite_file = f"{datetime.now().strftime("%Y%m%d_%H%M%S")}.README.md"
        r = self.client.upload(composite_file, url=url)

    def test_upload_pdf(self):
        pdf_path = resolve(__file__, '../fixtures/empty.pdf')
        self.client.upload(None, path=pdf_path)

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
        for doc in self.client.list_documents():
            # doc has content, can be lengthy
            print(doc['name'])

    def test_has(self):
        name = 'Admission - Technological and Higher Education Institute of Hong Kong.html'
        self.assertTrue(self.client.has_document(name))
        self.assertFalse(self.client.has_document('README'))

    def test_exist(self):
        doc_id = '3568dd90-fe30-4df3-8cc3-9f8a1cb9ee06'
        doc = Document(self.client, doc_id)
        self.assertTrue(doc.exist())
        doc_id = doc_id + '1'
        doc = Document(self.client, doc_id)
        self.assertFalse(doc.exist())

    def test_chunks(self):
        doc_id = '3568dd90-fe30-4df3-8cc3-9f8a1cb9ee06'
        doc = Document(self.client, doc_id)
        for chunk in doc.list_chunks():
            print(chunk['sign_content'])

    def test_chunk_get(self):
        doc_id = 'a9aff11c-f7e5-42fe-84e0-f21b522a68f9'
        doc = Document(self.client, doc_id)
        chunk_id = 'aa05539b-052e-4ec2-b8af-2067295423a2'
        chunk = Chunk(doc, chunk_id)
        chunk_data = chunk.get()
        self.assertIn('[![](', chunk_data['content'])  # how image, link are stored

    def test_del(self):
        doc_id = '6006f9db-4e7b-4760-a5b5-b8894ac8914c'
        doc = Document(self.client, doc_id)
        doc.delete()

class ChatAppTest(unittest.TestCase):
    api_key = os.getenv('APP_API_KEY') or 'app-fZVszIQWFFSUBLiSR2DE7Un3'

    def test_list_feedback(self):
        f = Feedbacks(self.api_key)
        for feedback in f.list_feedbacks():
            print(feedback['content'])

    def test_messages(self):
        c = Conversation(self.api_key, '999196d8-0842-4617-adcf-aa46e0808404')
        with self.assertRaises(HTTPError) as context:
            c.paginate_messages('f96b5cfc-7006-4afe-b8fe-e0e04374d40f')
        self.assertEqual(context.exception.response.status_code, 404)  # security isolation

    def test_agent_chat(self):
        me = '45bdc865-6d71-40ab-8892-af53906362fa'
        api_key = os.getenv('AGENT_API_KEY')
        c = Conversation(api_key, me)
        r = c.agent_chat("What are the specs of the iPhone 13 Pro Max?")
        print(r)
    def test_bot_chat(self):
        me = '45bdc865-6d71-40ab-8892-af53906362fa'
        api_key = os.getenv('BOT_API_KEY')
        c = Conversation(api_key, me)
        r = c.bot_chat("What are the specs of the iPhone 13 Pro Max?")
        print(r)


if __name__ == '__main__':
    unittest.main()
