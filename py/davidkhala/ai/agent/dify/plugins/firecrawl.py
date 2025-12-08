from davidkhala.ai.agent.dify.plugins import AbstractDataSource


class DataSourceOutput(AbstractDataSource):
    datasource_type = "website_crawl"
    source_url: str
    description: str
    title: str
    content: str


class Console(DataSourceOutput):
    credential_id: str
