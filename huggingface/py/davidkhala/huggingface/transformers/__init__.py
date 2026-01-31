from transformers import pipeline
from davidkhala.ai.model import MessageDict


class Pipeline:
    def __init__(self, task, model: str):
        self._ = pipeline(task, model, trust_remote_code=True)
        self.task = task

    def call(self, inputs: list[MessageDict] | str):
        results = self._(inputs)
        match self.task:
            case "text-generation":
                for r in results:
                    yield r['generated_text']
