from time import sleep

from requests.cookies import RequestsCookieJar

from davidkhala.ai.agent.dify.ops.console import API
from davidkhala.ai.agent.dify.common import IndexingStatus

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