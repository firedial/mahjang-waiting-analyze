from dataclasses import dataclass
from typing import ClassVar, Optional

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

    def sum(self) -> int:
        return sum(self.hand)

    def getRemainTileCount(self, index: int) -> int:
        if index < 0 or index >= self.HAND_LENGTH:
            raise ValueError("Invalid index.")

        return self.MAX_TILE_COUNT - self.hand[index]

    # @todo 返り値の型を付ける
    def addTile(self, index: int):
        if index < 0 or index >= self.HAND_LENGTH:
            raise ValueError("Invalid index.")

        resultHand = self.hand.copy()
        resultHand[index] += 1
        if resultHand[index] > self.MAX_TILE_COUNT:
            return None

        return Hand(resultHand)
