from __future__ import annotations

from typing import Iterable, TypedDict, Optional

from davidkhala.ai.agent.dify.base import API


class DatasetDict(TypedDict):
    id:str
    name:str
    description:str
    provider:str
    permission:str
    data_source_type:str
    indexing_technique:str
    doc_form:str
    runtime_mode:str
    is_published:bool
    enable_api:bool
    # stats
    app_count:int
    document_count:int
    word_count:int
    total_documents:int
    total_available_documents:int
    # embedding
    embedding_available:bool
    embedding_model:str
    embedding_model_provider:str
    retrieval_model_dict:dict
    external_retrieval_model:dict
    external_knowledge_info:dict


class Dataset(API):
    def __init__(self, api_key: str, base_url="https://api.dify.ai/v1"):
        super().__init__(api_key, base_url)
        self.base_url = f"{self.base_url}/datasets"


    class Iterator(Iterable):
        def __iter__(self):
            return self

        def __init__(self, d:Dataset, r):
            self.response = r
            self.client = d
        def __next__(self):
            if self.response and not self.response['has_more']:
                raise StopIteration
            self.response = self.client.list()
            return self.response['data']

    def list(self):

        return self.request(self.base_url, "GET")
    def list_all(self) -> Iterable[DatasetDict]:
        return Dataset.Iterator(self, None)