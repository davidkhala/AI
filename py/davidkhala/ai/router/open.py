import requests

models = [
    "openrouter/cypher-alpha:free",
    "mistralai/mistral-small-3.2-24b-instruct",
    "deepseek/deepseek-r1-0528-qwen3-8b",
    "deepseek/deepseek-r1-0528",
]
"""
free models
"""


class OpenRouter:
    def __init__(self, api_key: str,
                 models: list[str] = ["openrouter/cypher-alpha:free"],
                 *,
                 leaderboard: dict = None,
                 ):

        self.leaderboard = leaderboard
        self.models = models
        self.api_key = api_key

    def post(self, prompt, system_prompt: str = None):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        if self.leaderboard is not None:
            headers["HTTP-Referer"] = self.leaderboard['url'],  # Optional. Site URL for rankings on openrouter.ai.
            headers["X-Title"] = self.leaderboard['name'],  # Optional. Site title for rankings on openrouter.ai.
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        if system_prompt is not None:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        json = {
            "messages": messages
        }
        if len(self.models) > 1:
            json["models"] = self.models
        else:
            json["model"] = self.models[0]

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=json)
        response['provider']
        return response.json()
