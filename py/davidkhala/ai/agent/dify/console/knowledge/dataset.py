from time import sleep

from davidkhala.ai.agent.dify.console.session import ConsoleDerived
from davidkhala.ai.agent.dify.const import IndexingStatus
from davidkhala.ai.agent.dify.interface import IndexingError


class Operation(ConsoleDerived):
    def website_sync(self, dataset: str, document: str, *, wait_until=True):
        """
        cannot be used towards a pipeline dataset. Otherwise, you will see error "no website import info found"
        """
        doc_url = f"{self.base_url}/datasets/{dataset}/documents/{document}"

        r = self.request(f"{doc_url}/website-sync", "GET")
        assert r == {"result": "success"}
        if wait_until:
            return self.wait_until(dataset, document)
        return None

    def retry(self, dataset: str, *documents: str, wait_until=True):
        """
        It cannot trigger rerun on success documents
        """
        url = f"{self.base_url}/datasets/{dataset}/retry"
        self.request(url, "POST", json={
            'document_ids': documents,
        })
        # response status code will be 204
        if wait_until:
            return [self.wait_until(dataset, document) for document in documents]
        return None

    def rerun(self, dataset: str, *documents: str):
        for document in documents:
            try:
                self.website_sync(dataset, document)
                assert False, "expect IndexingError"
            except IndexingError:
                pass
        return self.retry(dataset, *documents)

    def wait_until(self, dataset: str, document: str, *,
                   expect_status=None,
                   from_status=None,
                   interval=1
                   ):
        if not expect_status:
            expect_status = [IndexingStatus.FAILED, IndexingStatus.COMPLETED]
        url = f"{self.base_url}/datasets/{dataset}/documents/{document}/indexing-status"
        if from_status is None:
            from_status = [IndexingStatus.WAITING, IndexingStatus.PARSING]
        r = self.request(url, "GET")
        status = r['indexing_status']
        assert status in from_status, f"current status: {status}, expect: {from_status}"
        while status not in expect_status:
            sleep(interval)
            r = self.request(url, "GET")
            status = r['indexing_status']
        if status == IndexingStatus.FAILED: raise IndexingError(r['error'])
        return r
