import os
import unittest

from davidkhala.utils.syntax.path import resolve
from requests import HTTPError

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
        from datetime import datetime
        composite_file = f"{datetime.now().strftime("%Y%m%d_%H%M%S")}.README.md"
        r = self.client.upload(composite_file, url=url)

    def test_upload_pdf(self):
        pdf_path = resolve(__file__, '../fixtures/empty.pdf')
        self.client.upload(None, path=pdf_path)

    def test_update(self):
        ...  # FIXME cannot rename
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
        for doc in self.client.list_documents():
            # doc has content, can be length
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
        self.assertIn('[![](', chunk_data['content']) # how image, link are stored

    def test_del(self):
        doc_id = '6006f9db-4e7b-4760-a5b5-b8894ac8914c'
        doc = Document(self.client, doc_id)
        doc.delete()


from davidkhala.ai.agent.dify.api.app import Feedbacks, Conversation


class ChatAppTest(unittest.TestCase):
    api_key = os.getenv('APP_API_KEY')

    def test_list_feedback(self):
        f = Feedbacks(self.api_key)
        for feedback in f.list_feedbacks():
            print(feedback['content'])

    def test_messages(self):
        user = '999196d8-0842-4617-adcf-aa46e0808404'
        conversation_id = 'f96b5cfc-7006-4afe-b8fe-e0e04374d40f'
        c = Conversation(self.api_key, user)
        with self.assertRaises(HTTPError) as context:
            c.paginate_messages(conversation_id)
        self.assertEqual(context.exception.response.status_code, 404)  # security isolation


from davidkhala.ai.agent.dify.ops.db import DB
import json


@unittest.skipIf(os.getenv('CI'), "open source deployment only")
class LocalDeploymentTest(unittest.TestCase):
    def setUp(self):
        connection_str = "postgresql://postgres:difyai123456@localhost:5432/dify"
        self.db = DB(connection_str)
        dataset_id = 'a2c739f4-2c04-4c32-b30b-f2cc517fec86'
        self.dataset = Dataset.Instance(Dataset('dataset-E1hUZPcn1qLIt8tNI2Klb4SN', 'http://localhost/v1'), dataset_id)

    def test_properties(self):
        print(self.db.apps)
        print(self.db.accounts)
    def test_user_feedbacks(self):
        print(self.db.user_feedbacks())
    def test_generate_conversation_opener(self):
        from davidkhala.ai.openrouter import Client
        # config
        app_id = '4f3c212a-0dc8-4405-97ca-22914c79a21e'
        question_size = 3
        api_key = os.environ.get('OPENROUTER_API_KEY')
        self.openrouter = Client(api_key)
        self.openrouter.as_chat('minimax/minimax-m2')
        config = self.db.app_config(app_id)
        self.assertIsNotNone(config)
        print('current suggested_questions', config.suggested_questions)
        new_questions = []
        for d in self.db.hit_documents(question_size):
            dataset_id = d['dataset_id']
            document_id = d['document_id']
            content = d['content']
            questions = self.db.dataset_queries(dataset_id)
            prompt = f"""
            Based on below knowledge base document content, generate single question that user may ask against the content. 
            Don't assume user have document content as prior knowledge.
            You should learn and follow language style from sample questions listed below. And you respond generated question text only
            
            sample questions:
            {questions}  
            
            document content is:
            {content}
            """
            choices = self.openrouter.chat(prompt)
            new_questions.append(choices[0].strip())
        config.suggested_questions = json.dumps(new_questions)
        self.db.update_app_config(config)


if __name__ == '__main__':
    unittest.main()
