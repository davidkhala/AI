import os

from transformers import AutoModel, PreTrainedModel


class Model:
    @staticmethod
    def load(pretrained_model_name_or_path: str | os.PathLike[str]) -> PreTrainedModel:
        return AutoModel.from_pretrained(pretrained_model_name_or_path, trust_remote_code=True, dtype="auto")
