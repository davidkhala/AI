import os
import unittest
from pathlib import Path

from mistralai import SDKError

from davidkhala.ai.mistral.agent import Agents
from davidkhala.ai.mistral.ai import Client
from davidkhala.ai.mistral.file import Client as FileClient
from davidkhala.ai.mistral.ocr import Client as OCRClient, FieldProperties

api_key = os.environ.get("API_KEY")


class AITest(unittest.TestCase):

    def setUp(self):
        self.client = Client(api_key)

    def test_chat(self):
        self.client.as_chat()
        message = "Who is the best French painter? Answer in one short sentence."
        print(self.client.chat(message))

    def test_live_chat(self):
        agents = Agents(api_key)
        agents.as_chat()
        agent = agents.create('football', web_search="web_search")
        message = "Who won the last European Football cup?"
        outputs, _ = agents.chat(agent.id, message)
        for out in outputs:
            print('--')
            print(out)

    def test_embedded(self):
        self.client.as_embeddings()
        r = self.client.encode("Embed this sentence.", "As well as this one.")
        print(r)

    def test_models(self):
        models = self.client.models
        self.assertGreaterEqual(len(models), 66)
        print(models)


class FileTest(unittest.TestCase):
    def setUp(self):
        self.client = FileClient(api_key)

    def test_list(self):
        print(self.client.ls())

    def test_upload(self):
        with self.assertRaises(SDKError) as e:
            self.client.upload(Path(__file__).parent / "fixtures" / "empty.jsonl")
        self.assertEqual(422, e.exception.status_code)
        self.assertEqual(
            '{"detail": "Invalid file format.", "description": "Found 1 error in this file. You can view supported formats here: https://docs.mistral.ai/capabilities/finetuning.", "errors": [{"message": "1 validation error for FinetuningMessages messages   Input should be a valid list [type=list_type, input_value={}, input_type=dict]     For further information visit https://errors.pydantic.dev/2.11/v/list_type", "line_number": 1}]}',
            e.exception.body)


class OCRTest(unittest.TestCase):
    def setUp(self):
        self.client = OCRClient(api_key)

    def test_extract(self):
        file = Path(__file__).parent / "fixtures" / "ilum.png"
        print(self.client.process(file))

    def test_entity(self):
        file = Path(__file__).parent / "fixtures" / "transcript.png"
        schema = {
            'Student': FieldProperties(required=True),
            'Date of Birth': FieldProperties(required=True),
            'Weighted GPA': FieldProperties(required=True),
            'Gender': FieldProperties(required=True),
            'Credits Earned': FieldProperties(),
        }

        r = self.client.process(file, schema)
        self.assertDictEqual(
            {'Student': 'Teddy Roosevelt', 'Date of Birth': 'Oct 27, 1910', 'Weighted GPA': '3.78/4.00',
             'Gender': 'Male', 'Credits Earned': '23.00'}, r)


if __name__ == "__main__":
    unittest.main()
