import runpy
from typing import Union, Literal

from openai import OpenAI, AsyncOpenAI

from davidkhala.ai.model import AbstractClient
from davidkhala.ai.model.chat import on_response


class Client(AbstractClient):
    client: OpenAI
    encoding_format: Literal["float", "base64"] = "float"
    n = 1

    def connect(self):
        try:
            type(self).models.fget(self)
            return True
        except:  # TODO make specific
            return False

    @property
    def models(self):
        return self.client.models.list()

    def encode(self, *_input: str) -> list[list[float]]:
        response = self.client.embeddings.create(
            model=self.model,
            input=list(_input),
            encoding_format=self.encoding_format
        )
        return [item.embedding for item in response.data]

    def chat(self, *user_prompt, **kwargs):

        messages = [
            *self.messages,
        ]
        for prompt in user_prompt:
            message = {
                "role": "user"
            }
            if type(prompt) == str:
                message['content'] = prompt
            elif type(prompt) == dict:
                message['content'] = [
                    {"type": "text", "text": prompt['text']},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": prompt['image_url'],
                        }
                    },
                ]
            messages.append(message)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            n=self.n,
            **kwargs
        )

        return on_response(response, self.n)

    def close(self):
        self.client.close()


def with_opik(instance: Union[OpenAI, AsyncOpenAI]):
    from opik.integrations.openai import track_openai
    runpy.run_path('../opik.py')
    return track_openai(instance)
