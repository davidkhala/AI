from time import sleep

from davidkhala.utils.http_request.stream import as_sse
from pydantic import BaseModel
from requests.cookies import RequestsCookieJar

from davidkhala.ai.agent.dify.common import IndexingStatus, IndexingError
from davidkhala.ai.agent.dify.ops.console import API
from davidkhala.ai.agent.dify.ops.db.orm import Node


class ConsoleKnowledge(API):
    def __init__(self, cookies: RequestsCookieJar,
                 *,
                 base_url='http://localhost'):
        super().__init__(base_url)
        self.session.cookies = cookies


class Datasource(ConsoleKnowledge):
    """step 1: Choose a Data Source"""

    class FirecrawlOutput(BaseModel):
        source_url: str
        description: str
        title: str
        credential_id: str
        content: str

    def run_firecrawl(self, pipeline: str, node: Node,
                      *,
                      inputs: dict,
                      credential_id: str
                      ):

        url = f"{self.base_url}/rag/pipelines/{pipeline}/workflows/published/datasource/nodes/{node.id}/run"

        response = self.session.post(url, stream=True, json={
            'inputs': inputs,
            'datasource_type': node.datasource_type,
            'credential_id': credential_id,
            "response_mode": "streaming"
        }, headers={
            'x-csrf-token': self.session.cookies.get("csrf_token")
        })
        # TODO still ugly on add-hoc
        for data in as_sse(response):
            event = data['event']
            if event == 'datasource_completed':
                return data['data']
            else:
                assert event == 'datasource_processing'
                print(data)
        return None

    def upload(self):
        "http://localhost/console/api/files/upload?source=datasets"
        # TODO
        "form data"
        {
            "file": "body"
        }
        r = {
            "id": "3898db5b-eb72-4f11-b507-628ad5d28887",
            "name": "Professional Diploma Meister Power Electrical Engineering - Technological and Higher Education Institute of Hong Kong.html",
            "size": 254362,
            "extension": "html",
            "mime_type": "text\/html",
            "created_by": "dbd0b38b-5ef1-4123-8c3f-0c82eb1feacd",
            "created_at": 1764943811,
            "source_url": "\/files\/3898db5b-eb72-4f11-b507-628ad5d28887\/file-preview?timestamp=1764943811&nonce=43b0ff5a13372415be79de4cc7ef398c&sign=7OJ2wiVYc4tygl7yvM1sPn7s0WXDlhHxgX76bsGTD94%3D"
        }


class Operation(ConsoleKnowledge):
    def website_sync(self, dataset, document, *, wait_until=True):
        """
        cannot be used towards a pipeline dataset. Otherwise, you will see error "no website import info found"
        """
        doc_url = f"{self.base_url}/datasets/{dataset}/documents/{document}"

        r = self.request(f"{doc_url}/website-sync", "GET")
        assert r == {"result": "success"}
        if wait_until:
            status = None
            while status not in [IndexingStatus.FAILED, IndexingStatus.COMPLETED]:
                sleep(1)
                r = self.request(f"{doc_url}/indexing-status", "GET")
                status = r['indexing_status']
            if status == IndexingStatus.FAILED: raise IndexingError(r['error'])
            return r
        return None


class Load(ConsoleKnowledge):
    """
    Processing Documents
    """

    def run(self, pipeline: str, node: Node, inputs: dict, datasource_info_list: list[dict]):
        # TODO test
        url = f"{self.base_url}/rag/pipelines/{pipeline}/workflows/published/run"
        return self.request(url, "POST", json={
            'inputs': inputs,
            'start_node_id': node.id,
            'is_preview': False,
            'response_mode': "blocking",
            "datasource_info_list": datasource_info_list,
            'datasource_type': node.datasource_type
        })
