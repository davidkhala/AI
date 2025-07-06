from davidkhala.ai.api import API

free = [
    "openrouter/cypher-alpha:free",
    "mistralai/mistral-small-3.2-24b-instruct",
    "deepseek/deepseek-r1-0528-qwen3-8b",
    "deepseek/deepseek-r1-0528",
]
"""
free models
"""


class OpenRouter(API):
    def __init__(self, api_key: str, models: list[str] = [free[0]], *,
                 leaderboard: dict = None):

        super().__init__(api_key, 'https://openrouter.ai/api')
        self.leaderboard = leaderboard
        self.models = models

    def pre_request(self, headers: dict, data: dict):
        if self.leaderboard is not None:
            headers["HTTP-Referer"] = self.leaderboard['url'],  # Optional. Site URL for rankings on openrouter.ai.
            headers["X-Title"] = self.leaderboard['name'],  # Optional. Site title for rankings on openrouter.ai.
        if len(self.models) > 1:
            data["models"] = self.models
        else:
            data["model"] = self.models[0]
