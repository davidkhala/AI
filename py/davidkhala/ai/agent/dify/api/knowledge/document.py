from __future__ import annotations

from typing import Iterable

import requests

from davidkhala.ai.agent.dify.api import API, Iterator
from davidkhala.ai.agent.dify.api.knowledge.dataset import Dataset
from davidkhala.ai.agent.dify.api.knowledge.model import ChunkDict


class Document(API):
    def __init__(self, d: Dataset.Instance, document_id: str):
        super().__init__(d.api_key, f"{d.base_url}/documents/{document_id}")

    def exist(self):
        try:
            self.get()
            return True
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return False
            else:
                raise e

    def get(self):
        return self.request(self.base_url, "GET")

    def paginate_chunks(self, page=1, size=20):
        return self.request(f"{self.base_url}/segments", "GET", params={
            'page': page,
            'limit': size
        })

    def list_chunks(self) -> Iterable[ChunkDict]:
        for chunk_batch in Iterator(self.paginate_chunks, None):
            for chunk in chunk_batch:
                yield chunk

    def delete(self):
        if self.exist():
            self.request(self.base_url, "DELETE")
