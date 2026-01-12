from abc import ABC
from typing import Protocol, TypedDict


class MessageDict(TypedDict):
    content: str | list
    role: str


class ClientProtocol(Protocol):
    api_key: str
    base_url: str
    model: str | None
    messages: list[MessageDict] | None


class AbstractClient(ABC, ClientProtocol):

    def as_chat(self, model: str, sys_prompt: str = None):
        self.model = model
        if sys_prompt is not None:
            self.messages = [MessageDict(role='system', content=sys_prompt)]

    def as_embeddings(self, model: str):
        self.model = model

    def chat(self, *user_prompt, **kwargs):
        ...

    def encode(self, *_input: str) -> list[list[float]]:
        ...

    def connect(self):
        ...

    def close(self):
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
