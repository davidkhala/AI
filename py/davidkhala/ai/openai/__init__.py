import runpy
from typing import Union

from openai import OpenAI, AsyncOpenAI


class OpenAIClient:
    def __init__(self, api_key, base_url=None):
        self.api_key = api_key
        self.base_url = base_url
    def as_azure(self, project):
        self.base_url = f"https://{project}.openai.azure.com/openai/v1/"
    def connect(self):
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        self.client.models.list()

def with_opik(instance: Union[OpenAI, AsyncOpenAI]):
    from opik.integrations.openai import track_openai
    runpy.run_path('../opik.py')
    return track_openai(instance)
