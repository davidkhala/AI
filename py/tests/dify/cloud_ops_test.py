import os
import unittest

from davidkhala.ai.agent.dify.api.knowledge.dataset import Dataset
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


        self.console.set_tokens(**{
            'csrf':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzAxMjgwMjUsInN1YiI6IjQ1YmRjODY1LTZkNzEtNDBhYi04ODkyLWFmNTM5MDYzNjJmYSJ9.C0iU0rwL9UD-bkbH9pdL0WJKsC4ziGJSCuuDhTwxnn0',
            'access':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNDViZGM4NjUtNmQ3MS00MGFiLTg4OTItYWY1MzkwNjM2MmZhIiwiZXhwIjoxNzcwMTI4MDI1LCJpc3MiOiJDTE9VRCIsInN1YiI6IkNvbnNvbGUgQVBJIFBhc3Nwb3J0In0.nuRJFmpySoi6jljrnGYxgl4FYuEPBaEb55QBbpWZx98',
        })

    def test_pipeline_dev(self):
        # TODO do a cloud version
        dataset_id = '8bae26cb-a2be-4487-8492-04554a4f7b8b'
        from davidkhala.ai.agent.dify.api.knowledge.dataset import Dataset
        from davidkhala.ai.agent.dify.console.knowledge.dataset import Operation
        from davidkhala.ai.agent.dify.console.knowledge.pipeline import Datasource, Pipeline
        from davidkhala.ai.agent.dify.console.plugin import ConsoleTool

        ds = Dataset.Instance(Dataset(self.api_key), dataset_id)
        p_id = ds.get().pipeline_id

        kb_console = Datasource(self.console)
        console_ops = Operation(self.console)
        console_tool = ConsoleTool(self.console)
        console_pipeline = Pipeline(self.console)
        credential_id = console_tool.credential_id_by('key', 'langgenius', "firecrawl")

        pipeline = console_pipeline.get(p_id)
        nodes = pipeline.graph.datasources
        node: NodeProtocol|None = None
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
        assert len(run_r.documents)==pages
        for document in run_r.documents:
            final = console_ops.wait_until(run_r.dataset.id, document.id,
                                           from_status=[IndexingStatus.WAITING, IndexingStatus.PARSING,
                                                        IndexingStatus.COMPLETED, IndexingStatus.FAILED])
            print(final)



if __name__ == '__main__':
    unittest.main()
