from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class Waiting:

    waitingCount: tuple[int, ...]
    isSendable: bool

    MAX_TILE_COUNT: ClassVar[int] = 4
    HAND_LENGTH: ClassVar[int] = 9

    def __init__(self, waitingCount: tuple[int, ...], isSendable: bool):
        if len(waitingCount) != self.HAND_LENGTH:
            raise ValueError("Wrong waitingCount length.")

        for tile in waitingCount:
            if tile > self.MAX_TILE_COUNT or tile < 0:
                raise ValueError("Wrong waitingCount count.")

        object.__setattr__(self, "waitingCount", waitingCount)
        object.__setattr__(self, "isSendable", isSendable)

    def isTempai(self) -> bool:
        return self.isSendable or sum(self.waitingCount) > 0

    def getWaitingTileCount(self) -> int:
        return len(list(filter(lambda x: x > 0, self.waitingCount)))
