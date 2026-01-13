from typing import Protocol, Any

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


def messages_from(*user_prompt: str) -> list[MessageDict]:
    return [MessageDict(role='user', content=_) for _ in user_prompt]
