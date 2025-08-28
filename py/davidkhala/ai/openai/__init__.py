import runpy
from typing import Union

from openai import OpenAI, AsyncOpenAI


def with_opik(instance: Union[OpenAI, AsyncOpenAI]):
    from opik.integrations.openai import track_openai
    runpy.run_path('../opik.py')
    return track_openai(instance)
