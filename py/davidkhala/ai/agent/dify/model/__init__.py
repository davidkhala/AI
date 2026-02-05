from pydantic import BaseModel

class ID(BaseModel):
    id: str

class User(ID):
    name: str
    email: str
