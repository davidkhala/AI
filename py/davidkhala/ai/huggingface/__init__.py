import os

from huggingface_hub import snapshot_download, InferenceClient
from davidkhala.ai.model import AbstractClient
from davidkhala.ai.model.chat import messages_from, on_response

def clone(git_dir: os.PathLike,
          *,
          owner: str|None = None,
          repository: str|None = None,
          repo_id: str|None = None,
          **kwargs
          ) -> str:
    if not repo_id:
        repo_id = f"{owner}/{repository}"
    return snapshot_download(
        repo_id=repo_id,
        local_dir=git_dir,
        local_dir_use_symlinks=False,
        **kwargs
    )


class Client(AbstractClient):
    def __init__(self, api_key: str):
        self.client = InferenceClient(
            api_key=api_key,
        )
    def chat(self, *user_prompt, **kwargs):
        r = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages + messages_from(*user_prompt),
            # TODO standardize image user prompt
            **kwargs,
        )
        return on_response(r, n=self.n)


