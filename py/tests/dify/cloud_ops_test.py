import os
import unittest

from davidkhala.ai.agent.dify.api.knowledge import Dataset
from davidkhala.ai.agent.dify.common import IndexingStatus
from tests.util import prepare_logger


class DocumentTestCase(unittest.TestCase):
    def setUp(self):
        self.api_key = os.getenv('KB_API_KEY')
        dataset_id = '8bae26cb-a2be-4487-8492-04554a4f7b8b'
        self.client = Dataset.Instance(Dataset(self.api_key), dataset_id)
        self.logger = prepare_logger('py/tests/dify/cloud_doc.log')
    def test_del_pending(self):
        for doc in self.client.list_documents():
            # doc has content, can be lengthy
            if doc['indexing_status'] == IndexingStatus.WAITING:
                print(doc)
                self.logger.warning(doc)


if __name__ == '__main__':
    unittest.main()
