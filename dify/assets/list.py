import requests
from typing import Iterable, Callable, Optional


class Iterator(Iterable):
    def __iter__(self):
        return self

    def __init__(self, get_fn: Callable, r):
        self.fn = get_fn
        self.response = r

    def __next__(self):
        if self.response and not self.response['has_more']:
            raise StopIteration
        self.response = self.fn()
        return self.response['data']


def default_on_response(response: requests.Response) -> Optional[dict]:
    if not response.ok:
        response.raise_for_status()
    else:
        return response.json()


def main(dataset_id: str, base_url: str, api_key: str):
    url = f"{base_url}/datasets/{dataset_id}/documents"

    def list_documents():
        return default_on_response(requests.get(url, headers={
            'Authorization': f"Bearer {api_key}"
        }))

    docs = []
    for mat in Iterator(list_documents, None):
        for doc in mat:
            docs.append(doc)
    return {
        "result": docs,
    }
