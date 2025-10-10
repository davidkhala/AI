from typing import TypedDict, Optional

from davidkhala.ai.api import API


class Leaderboard(TypedDict):
    url: Optional[str]
    name: Optional[str]


class OpenRouter(API):
    @property
    def free_models(self) -> list[str]:
        return list(
            map(lambda model: model['id'],
                filter(lambda model: model['id'].endswith(':free'), self.list_models())
                )
        )

    def __init__(self, api_key: str, *models: str, **kwargs):

        super().__init__(api_key, 'https://openrouter.ai/api')

        if 'leaderboard' in kwargs and type(kwargs['leaderboard']) is dict:
            self.headers["HTTP-Referer"] = kwargs['leaderboard']['url']  # Site URL for rankings on openrouter.ai.
            self.headers["X-Title"] = kwargs['leaderboard']['name']  # Site title for rankings on openrouter.ai.
        if not models:
            models = [self.free_models[0]]
        self.models = models

    def chat(self, *user_prompt: str, **kwargs):
        if len(self.models) > 1:
            kwargs["models"] = self.models
        else:
            kwargs["model"] = self.models[0]

        return super().chat(*user_prompt, **kwargs)