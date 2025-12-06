from pydantic import BaseModel

class DataSource:
    type = "website_crawl"
    class Output(BaseModel):
        source_url: str
        description: str
        title: str
        credential_id: str
        content: str