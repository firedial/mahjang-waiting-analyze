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
