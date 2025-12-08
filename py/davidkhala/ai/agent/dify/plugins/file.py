from pydantic import BaseModel

from davidkhala.ai.agent.dify.plugins import AbstractDataSource


class FileModel(BaseModel):
    name: str
    size: int
    type: str
    extension: str
    mime_type: str
    transfer_method: str
    url: str
    related_id: str


class DataSourceOutput(AbstractDataSource):
    datasource_type = "local_file"
    file: FileModel
