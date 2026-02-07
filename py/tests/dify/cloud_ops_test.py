import os
import unittest

from davidkhala.ai.agent.dify.api.knowledge.dataset import Dataset
from davidkhala.ai.agent.dify.api.knowledge.document import Document
from davidkhala.ai.agent.dify.console.knowledge.dataset import DocumentOperation, DocumentMetadata
from davidkhala.ai.agent.dify.const import IndexingStatus
from davidkhala.ai.agent.dify.model.workflow import NodeProtocol
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


class ConsoleTestCase(unittest.TestCase):
    def setUp(self):
        self.api_key = os.getenv('KB_API_KEY')

        from davidkhala.ai.agent.dify.console.session import ConsoleUser
        self.console = ConsoleUser(base_url='https://cloud.dify.ai')

        self.console.set_tokens(
            csrf='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzA0NzAwNTMsInN1YiI6IjQ1YmRjODY1LTZkNzEtNDBhYi04ODkyLWFmNTM5MDYzNjJmYSJ9.s5sn-lBIuNwv1d0tyT3Hoi5UuQzAwhuS8fHvPwIflxo',
            access='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNDViZGM4NjUtNmQ3MS00MGFiLTg4OTItYWY1MzkwNjM2MmZhIiwiZXhwIjoxNzcwNDcwMDUzLCJpc3MiOiJDTE9VRCIsInN1YiI6IkNvbnNvbGUgQVBJIFBhc3Nwb3J0In0.orO-HD8LIR6RRbSAh3JDuWVe8JZEUf2cd-yuKDKbai0',
        )
        self.metadata = DocumentMetadata(self.console, '8bae26cb-a2be-4487-8492-04554a4f7b8b') # Thei one details

    def test_list_metadata(self):
        r = self.metadata.list()
        print(r)

    def test_set_metadata(self):

        documents = [
            'e97a986b-9613-4f09-a8b2-d069f94bd1f9',
            "d30300cf-a11c-4018-8b3c-07820bec11c0",
            "38eb6e0c-ca99-40f9-a3d0-96890ef3d16b",
            "4e1738a6-0a8c-4953-9c72-135139302665",
            "704c0765-d524-4817-8cf3-5a8366c38907"
        ]  # master
        metadata = {
            'level': 'postgraduate'
        }
        self.metadata.set(*documents, metadata=metadata)
        # ensure
        self.client = Dataset.Instance(Dataset(self.api_key), self.metadata.dataset)
        for doc_id in documents:
            doc = Document(self.client, doc_id)
            metadata_r = doc.get('only').custom_metadata
            assert len(metadata_r) == 1

            self.assertDictEqual(metadata_r[0], metadata)


    def test_pipeline_dev(self):
        # TODO do a cloud version
        dataset_id = '8bae26cb-a2be-4487-8492-04554a4f7b8b'
        from davidkhala.ai.agent.dify.api.knowledge.dataset import Dataset

        from davidkhala.ai.agent.dify.console.knowledge.pipeline import Datasource, Pipeline
        from davidkhala.ai.agent.dify.console.plugin import ConsoleTool

        ds = Dataset.Instance(Dataset(self.api_key), dataset_id)
        p_id = ds.get().pipeline_id

        kb_console = Datasource(self.console)

        console_tool = ConsoleTool(self.console)
        console_pipeline = Pipeline(self.console)
        credential_id = console_tool.credential_id_by('key', 'langgenius', "firecrawl")

        pipeline = console_pipeline.get(p_id)
        nodes = pipeline.graph.datasources
        node: NodeProtocol | None = None
        for _ in nodes:
            if _.data.title == 'Firecrawl':
                node = _
                break
        pages = 1
        sources_r = kb_console.run_firecrawl(p_id, node, inputs={
            "url": "https://thei.edu.hk/",
            "subpage": False,
            "pages": pages
        }, credential_id=credential_id)

        print('--run_firecrawl completed')
        from davidkhala.ai.agent.dify.plugins.firecrawl import Console

        datasource_info_list = []
        for source in sources_r:
            source['credential_id'] = credential_id
            source['title'] = source['source_url']
            Console.model_validate(source)  # schema validation
            datasource_info_list.append(source)

        run_r = pipeline.async_run(p_id, node, inputs={
            'child_length': 512
        }, datasource_info_list=datasource_info_list)
        # wait until
        assert len(run_r.documents) == pages
        console_ops = DocumentOperation(self.console, run_r.dataset.id)
        for document in run_r.documents:
            final = console_ops.wait_until(document.id,
                                           from_status=[IndexingStatus.WAITING, IndexingStatus.PARSING,
                                                        IndexingStatus.COMPLETED, IndexingStatus.FAILED])
            print(final)


if __name__ == '__main__':
    unittest.main()
