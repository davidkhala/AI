from typing import Protocol, Any


class ClientProtocol(Protocol):
    api_key: str
    base_url: str


class ModelAware:
    def __init__(self):
        self.model: str | None = None


class SDKProtocol(Protocol):
    client: Any


class Connectable:
    def connect(self) -> bool: ...

    def close(self): ...

    def __enter__(self):
        assert self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
