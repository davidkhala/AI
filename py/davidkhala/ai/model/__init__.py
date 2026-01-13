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

class ChatProtocol(Protocol):
    def as_chat(self, model: str, sys_prompt: str = None):...
    def chat(self, *user_prompt, **kwargs):...
class AbstractClient(ABC, ClientProtocol, ChatProtocol):

    def __init__(self):
        self.model = None
        self.messages = []

    def as_chat(self, model: str, sys_prompt: str = None):
        self.model = model
        if sys_prompt is not None:
            self.messages = [MessageDict(role='system', content=sys_prompt)]

    def as_embeddings(self, model: str):
        self.model = model

    def encode(self, *_input: str) -> list[list[float]]:
        ...

    def connect(self)-> bool:
        ...

    def close(self):
        ...

    def __enter__(self):
        assert self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
