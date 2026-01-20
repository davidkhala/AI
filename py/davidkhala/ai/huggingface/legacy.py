from huggingface_hub import InferenceApi
from davidkhala.utils.syntax.compat import deprecated
@deprecated("`from huggingface_hub import InferenceClient` is preferred since 2024")
class API:
    def __init__(self, token):
        self.inference = None
        self.token = token

    def as_model(self, repo_id):
        self.inference = InferenceApi(repo_id=repo_id, token=self.token)

    def call(self, **kwargs):
        return self.inference(**kwargs)
