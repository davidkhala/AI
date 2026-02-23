from typing import Union


def bind(instance: Union["openai.OpenAI", "openai.AsyncOpenAI"]):
    from opik.integrations.openai import track_openai
    start()
    return track_openai(instance)


def start():
    from opik import configure
    configure()
