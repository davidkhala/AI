from pydantic import BaseModel

class JsonEntry(BaseModel):
    data: list

class Output(BaseModel):
    """Class for result of a Dify node"""
    text: str
    files: list
    json: list[JsonEntry]
