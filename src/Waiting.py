from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class Waiting:

    waitings: tuple[bool, ...]

    HAND_LENGTH: ClassVar[int] = 9

    def __init__(self, waitings: tuple[bool, ...]):
        if len(waitings) != self.HAND_LENGTH:
            raise ValueError("Wrong waitings length.")

        object.__setattr__(self, "waitings", waitings)

    def getWaitingTileCount(self) -> int:
        return len(list(filter(lambda x: x, self.waitings)))

    def getWaitingAddTile(self, index):
        return Waiting(self.waitings[:index] + (True, ) + self.waitings[(index + 1):])

    def __eq__(self, other) -> bool:
        return self.waitings == other.waitings

    def __ne__(self, other) -> bool:
        return self != other
