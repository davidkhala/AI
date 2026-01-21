from typing import Protocol, Any, Iterable

from davidkhala.ai.model import MessageDict


class MessageProtocol(Protocol):
    content: str | Any


class ChoiceProtocol(Protocol):
    message: MessageProtocol


class ChoicesAware(Protocol):
    choices: list[ChoiceProtocol]


def on_response(response: ChoicesAware, n: int):
    contents = [choice.message.content for choice in response.choices]
    assert len(contents) == n
    return contents


def messages_from(*user_prompt: str|dict) -> Iterable[MessageDict]:

    for _ in user_prompt:
        message = MessageDict(role='user', content=None)
        if type(_) == str:
            message.content = _
        elif type(_) == dict:
            message.content = [{"type": "text", "text": _['text']}]
            message.content.extend({"type": "image_url","image_url": {"url": i}} for i in _['image_url'])
        yield message

