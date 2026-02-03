from pydantic import BaseModel

from davidkhala.ai.agent.dify.const import IndexingStatus


class Document(BaseModel):
    id: str
    position: int
    data_source_type: str
    data_source_info: dict[str, str]
    name: str
    indexing_status: IndexingStatus
    error: str | None
    enabled: bool


class Dataset(BaseModel):
    id: str
    name: str
    description: str
