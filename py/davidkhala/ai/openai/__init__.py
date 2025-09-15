import runpy
from abc import ABC
from typing import Union, Optional

from openai import OpenAI, AsyncOpenAI


class Client(ABC):
    api_key:str
    base_url:str
    model:Optional[str]
    messages= []
    client:OpenAI
    def as_chat(self, model, sys_prompt: str = None):
        self.model = model
        if sys_prompt is not None:
            self.messages = [{"role": "system", "content": sys_prompt}]

    def connect(self):
        self.client.models.list()
    def chat(self, user_prompt, image: str= None):

        message = {
            "role": "user"
        }
        if image is None:
            message['content'] = user_prompt
        else:
            message['content'] = [
                {"type": "text", "text": user_prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image,
                    }
                },
            ]
        response=  self.client.chat.completions.create(
            model=self.model ,
            messages=[
                *self.messages,
                message
            ],
        )
        return response.choices[0].message.content
    def disconnect(self):
        self.client.close()





def with_opik(instance: Union[OpenAI, AsyncOpenAI]):
    from opik.integrations.openai import track_openai
    runpy.run_path('../opik.py')
    return track_openai(instance)
