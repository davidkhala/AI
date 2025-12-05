from time import sleep

from requests.cookies import RequestsCookieJar

from davidkhala.ai.agent.dify.common import IndexingStatus
from davidkhala.ai.agent.dify.ops.console import API


class ConsoleKnowledge(API):
    def __init__(self, cookies: RequestsCookieJar,
                 *,
                 base_url='http://localhost'):
        super().__init__(base_url)
        self.session.cookies = cookies

    def website_sync(self, dataset, document, *, wait_until=True):
        doc_url = f"{self.base_url}/datasets/{dataset}/documents/{document}"
        self.options['headers']['x-csrf-token'] = self.session.cookies.get("csrf_token")

        r = self.request(f"{doc_url}/website-sync", "GET")
        assert r == {"result": "success"}
        if wait_until:
            status = None
            while status not in [IndexingStatus.FAILED, IndexingStatus.COMPLETED]:
                r = self.request(f"{doc_url}/indexing-status", "GET")
                status = r['indexing_status']
                sleep(1)
            return r
        return None

    def run(self, pipeline, node,
            *,
            inputs: dict,
            datasource_type='website_crawl',
            credential_id: str
            ):
        """run in Choose a Data Source"""
        url = f"{self.base_url}/rag/pipelines/{pipeline}/workflows/published/datasource/nodes/{node}/run"

        response = self.session.post(url, stream=True, json={
            'inputs': inputs,
            'datasource_type': datasource_type,
            'credential_id': credential_id,
            "response_mode": "streaming"
        })
        for line in response.iter_lines():
            if line:
                print("Received:", line.decode())

    def upload(self):
        "http://localhost/console/api/files/upload?source=datasets"
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
