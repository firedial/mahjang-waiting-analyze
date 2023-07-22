from dataclasses import dataclass
from typing import ClassVar

@dataclass(frozen=True)
class Hand:

    hand: list[int]
    MAX_TILE_COUNT: ClassVar[int] = 4
    HAND_LENGTH: ClassVar[int] = 9

    def __init__(self, hand: list[int]):
        if len(hand) != self.HAND_LENGTH:
            raise ValueError("Wrong hand length.")

        for tile in hand:
            if tile > self.MAX_TILE_COUNT or tile < 0:
                raise ValueError("Wrong tile count.")

        object.__setattr__(self, "hand", hand)

    def length(self) -> int:
        return len(self.hand)
