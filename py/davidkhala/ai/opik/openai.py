from opik.integrations.openai.opik_tracker import OpenAIClient

from davidkhala.ai.opik import start


def bind(instance: OpenAIClient):
    from opik.integrations.openai import track_openai
    start()
    return track_openai(instance)
