from huggingface_hub import InferenceClient

from davidkhala.ai.model import SDKProtocol
from davidkhala.ai.model.chat import on_response, ChatAware


class Client(ChatAware, SDKProtocol):
    def __init__(self, api_key: str):
        super().__init__()
        self.client = InferenceClient(
            api_key=api_key,
        )

    def chat(self, *user_prompt, **kwargs):
        r = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages_from(*user_prompt),
            n=self.n,
            **kwargs,
        )
        return on_response(r, n=self.n)

    def fill(self, template: str):
        assert "[MASK]" in template
        return [_.sequence for _ in self.client.fill_mask(template, model=self.model)]
