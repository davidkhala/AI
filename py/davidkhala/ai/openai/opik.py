import runpy

from openai import OpenAI, AsyncOpenAI
from typing import Union


def bind(instance: Union[OpenAI, AsyncOpenAI]):
    from opik.integrations.openai import track_openai
    runpy.run_path('../opik.py')
    return track_openai(instance)