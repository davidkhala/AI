from davidkhala.ai.api import API


class SiliconFlow(API):
    @property
    def free_models(self) -> list[str]:
        return [
            'deepseek-ai/DeepSeek-R1-0528-Qwen3-8B',
            'deepseek-ai/DeepSeek-R1-Distill-Qwen-7B',
        ]

    def __init__(self, api_key: str, model: str):
        super().__init__(api_key, 'https://api.siliconflow.cn')
        self.model = model
    def pre_request(self, headers: dict, data: dict):
        super().pre_request(headers, data)