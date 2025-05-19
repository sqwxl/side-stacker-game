from abc import ABC
from dataclasses import dataclass
from typing import Any, ClassVar, TypedDict


@dataclass(frozen=True)
class Payload(ABC):
    pass


@dataclass(frozen=True)
class PlayPayload(Payload):
    col: int
    row: int

    def __iter__(self):
        return iter((self.col, self.row))


@dataclass(frozen=True)
class Action(ABC):
    name: ClassVar[str]
    payload: Payload


@dataclass(frozen=True)
class PlayAction(Action):
    name: ClassVar[str] = "play"
    payload: PlayPayload


class RawAction(TypedDict):
    name: str
    payload: dict[str, Any]


def parse_action(obj: RawAction) -> Action:
    """
    obj: { "name": <action name>, "payload": <action payload> }
    """
    try:
        name = obj["name"]
        data = obj["payload"]

        match name:
            case PlayAction.name:
                return PlayAction(payload=PlayPayload(**data))
            case _:
                raise ValueError(f"Unknown action: {name}")
    except (KeyError, TypeError) as e:
        raise ValueError(f"Invalid message format: {e}")
