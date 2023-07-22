from dataclasses import dataclass
from typing import ClassVar

@dataclass(frozen=True)
class Waiting:

    waitingCount: list[int]
    atamaWaitingCount: int

    MAX_TILE_COUNT: ClassVar[int] = 4
    HAND_LENGTH: ClassVar[int] = 9

    def __init__(self, waitingCount: list[int], atamaWaitingCount: int):
        if len(waitingCount) != self.HAND_LENGTH:
            raise ValueError("Wrong waitingCount length.")

        for tile in waitingCount:
            if tile > self.MAX_TILE_COUNT or tile < 0:
                raise ValueError("Wrong waitingCount count.")

        if atamaWaitingCount < 0 or atamaWaitingCount > 2:
            raise ValueError("Wrong atamaWaitingCount value.")

        object.__setattr__(self, "waitingCount", waitingCount)
        object.__setattr__(self, "atamaWaitingCount", atamaWaitingCount)

    def isTempai(self) -> bool:
        return sum(self.waitingCount) > 0

    def getWaitingTileCountWithAtama(self) -> int:
        return len(list(filter(lambda x: x > 0, self.waitingCount))) + self.atamaWaitingCount

    def __lt__(self, other):
        # あがり牌に昇格した場合(和了牌だが4枚使いだった場合)は待ちに関係する
        for (a, b) in zip(self.waitingCount, other.waitingCount):
            if a >= 1 and b == 0:
                return True

        return self.getWaitingTileCountWithAtama() != other.getWaitingTileCountWithAtama()
