from abc import ABC
from typing import Optional


class AbstractClient(ABC):
    api_key: str
    base_url: str
    model: Optional[str]
    messages = []

    def as_chat(self, model: str, sys_prompt: str = None):
        self.model = model
        if sys_prompt is not None:
            self.messages = [{"role": "system", "content": sys_prompt}]

    def chat(self, user_prompt: str, **kwargs):
        ...

    def connect(self):
        ...

    def disconnect(self):
        ...
