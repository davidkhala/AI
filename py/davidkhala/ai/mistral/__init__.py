from mistralai import Mistral


class Client:

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = Mistral(api_key=api_key)

    def __enter__(self):
        self.client.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.client.__exit__(exc_type, exc_val, exc_tb)
