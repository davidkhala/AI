import os
import unittest

import onnx
import onnxruntime

from davidkhala.huggingface import Client





class ClientTestCase(unittest.TestCase):

    def setUp(self):
        token = os.environ.get('PAT')
        self.client = Client(api_key=token)

    def test_qwen_chat(self):
        print(self.qwenvl("Hello, how are you?"))

    def qwenvl(self, text, url=None):
        self.client.as_chat("Qwen/Qwen3-VL-8B-Instruct")
        if url:
            from davidkhala.ai.model.chat import ImagePromptDict
            prompt = ImagePromptDict(
                text='Please validate if it is real. If it is too blur to be validated, reply uncertain',
                image_url=[url])
            return self.client.chat(prompt)
        else:
            return self.client.chat(text)

    def test_qwen_false_positive(self):
        url = "https://www.transcriptmaker.com/wp-content/uploads/2019/03/transcript8-1-791x1024.png"
        print(self.qwenvl(None, url))

    def test_false_negative(self):
        url = "https://www.transcriptmaker.com/wp-content/uploads/2019/03/transcript9_watermark.jpg"
        print(self.qwenvl(None, url))

    def test_true_positive(self):
        url = "https://cn9yc2hk0gzg.objectstorage.ap-singapore-1.oci.customer-oci.com/n/cn9yc2hk0gzg/b/data/o/HKU%20Transcript.jpg"
        print(self.qwenvl(None, url))



    def test_bert(self):
        self.client.as_chat("google-bert/bert-base-uncased")
        r = self.client.fill("The goal of life is [MASK].")
        print(r)
        r = self.client.fill("The answer to the universe is [MASK].")
        print(r)


if __name__ == '__main__':
    unittest.main()
