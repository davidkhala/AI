from typing import Optional, Literal

from openai import OpenAI

from davidkhala.ai.openai import Client


class NativeClient(Client):
    def __init__(self, api_key, base_url=None):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

    def chat(self, *user_prompt, web_search:Optional[Literal["low", "medium", "high"]]=None, **kwargs):
        opts = {
            **kwargs
        }
        if web_search:
            from openai.types.chat.completion_create_params import WebSearchOptions
            opts['web_search_options'] = WebSearchOptions(search_context_size=web_search)
        return super().chat(*user_prompt, **opts)
