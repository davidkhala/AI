from datetime import datetime
from time import sleep
from typing import Callable

from davidkhala.ai.agent.dify.api.knowledge.model import DocMetadataModel, MetadataType
from davidkhala.ai.agent.dify.console.session import ConsoleDerived, ConsoleUser
from davidkhala.ai.agent.dify.const import IndexingStatus
from davidkhala.ai.agent.dify.interface import IndexingError


class Operation(ConsoleDerived):
    def __init__(self, context: ConsoleUser, dataset: str):
        super().__init__(context)
        self.base_url = f"{context.base_url}/datasets/{dataset}"
        self.dataset = dataset


class DocumentOperation(Operation):

    def website_sync(self, document: str, *, wait_until=True):
        """
        for dataset with runtime_mode=standard
        cannot be used towards a pipeline dataset. Otherwise, you will see error "no website import info found"
        It can be used to force document into error status
        """

        r = self.request(f"{self.base_url}/documents/{document}/website-sync", "GET")
        assert r == {"result": "success"}
        if wait_until:
            return self.wait_until(document)
        return None

    def retry(self, *documents: str, wait_until=True):
        """
        It cannot trigger rerun on success documents
        """
        url = f"{self.base_url}/retry"
        self.request(url, "POST", json={
            'document_ids': documents,
        })
        # response status code will be 204
        if wait_until:
            return [self.wait_until(document) for document in documents]
        return None

    def rerun(self, *documents: str):
        for document in documents:
            try:
                self.website_sync(document)
                assert False, "expect IndexingError"
            except IndexingError:
                pass
        return self.retry(*documents)

    def wait_until(self, document: str, *,
                   expect_status=None,
                   from_status=None,
                   interval=1
                   ):
        # TODO this has public api version in https://docs.dify.ai/api-reference/documents/get-document-embedding-status-progress
        if not expect_status:
            expect_status = [IndexingStatus.FAILED, IndexingStatus.COMPLETED]
        url = f"{self.base_url}/documents/{document}/indexing-status"
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


class DocumentMetadata(Operation):
    def list(self) -> list[DocMetadataModel]:
        r = self.request(f"{self.base_url}/metadata", "GET")
        return [DocMetadataModel.model_validate(_) for _ in r['doc_metadata']]

    def add(self, _type: MetadataType, name: str) -> str:
        r = self.request(f"{self.base_url}/metadata", "POST", json={
            'type': _type, 'name': name
        })
        return r['id']

    def delete(self, metadata_id: str):
        self.request(f"{self.base_url}/metadata/{metadata_id}", "DELETE")

    def set(self, *documents: str, metadata: dict):
        url = f"{self.base_url}/documents/metadata"
        metadata_list = []
        datasets = self.list()

        for name, value in metadata.items():
            _type: MetadataType
            match value:
                case str():
                    _type = "string"
                case datetime():
                    _type = "time"
                    value = int(value.timestamp())
                case _:
                    _type = "number"
            _id = next((_.id for _ in datasets if _.name == name), None)
            if not _id:
                _id = self.add(_type, name)

            metadata_list.append({
                'id': _id,
                'type': _type,
                'name': name, 'value': value
            })
        self.request(url, "POST", json={
            'operation_data': [
                {'document_id': document, 'metadata_list': metadata_list, "partial_update": False}
                for document in documents
            ],
        })
