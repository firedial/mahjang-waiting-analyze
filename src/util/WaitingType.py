from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class WaitingType:

    isTanki: bool
    isShampon: bool
    isKanchan: bool
    # 34 で 2 待ちの時
    isRyanmenLeft: bool
    # 34 で 5 待ちの時
    isRyanmenRight: bool

    def __init__(self, isTanki: bool, isShampon: bool, isKanchan: bool, isRyanmenLeft: bool, isRyanmenRight: bool):
        object.__setattr__(self, "isTanki", isTanki)
        object.__setattr__(self, "isShampon", isShampon)
        object.__setattr__(self, "isKanchan", isKanchan)
        object.__setattr__(self, "isRyanmenLeft", isRyanmenLeft)
        object.__setattr__(self, "isRyanmenRight", isRyanmenRight)

    def hasWaiting(self):
        return self.isTanki or self.isShampon or self.isKanchan or self.isRyanmenLeft or self.isRyanmenRight

    def addShampon(self):
        return WaitingType(
            isTanki = self.isTanki,
            isShampon = True,
            isKanchan = self.isKanchan,
            isRyanmenLeft = self.isRyanmenLeft,
            isRyanmenRight = self.isRyanmenRight,
        )

    def addRyanmenLeft(self):
        return WaitingType(
            isTanki = self.isTanki,
            isShampon = self.isShampon,
            isKanchan = self.isKanchan,
            isRyanmenLeft = True,
            isRyanmenRight = self.isRyanmenRight,
        )

    def addRyanmenRight(self):
        return WaitingType(
            isTanki = self.isTanki,
            isShampon = self.isShampon,
            isKanchan = self.isKanchan,
            isRyanmenLeft = self.isRyanmenLeft,
            isRyanmenRight = True,
        )

    def __eq__(self, other) -> bool:
        return self.isTanki == other.isTanki and self.isShampon == other.isShampon and self.isKanchan == other.isKanchan and self.isRyanmenLeft == other.isRyanmenLeft and self.isRyanmenRight == other.isRyanmenRight

    def __ne__(self, other) -> bool:
        return not (self == other)
