from dataclasses import dataclass
from typing import ClassVar, Optional
from src.Suit import Suit
from src.Waiting import Waiting
import src.Remove as Remove
import src.Agari as Agari

@dataclass(frozen=True)
class Hand:

    suit: Suit
    isAtamaConnectedShuntsu: bool
    waiting: Waiting

    def __init__(self, suit: Suit, isAtamaConnectedShuntsu: bool = False):
        object.__setattr__(self, "waiting", Agari.getWaiting(suit))
        object.__setattr__(self, "suit", suit)
        object.__setattr__(self, "isAtamaConnectedShuntsu", isAtamaConnectedShuntsu)

    def isTempai(self) -> bool:
        return self.waiting.isTempai()

    def isBasicForm(self) -> bool:
        return self.suit.isBasicForm()

    def isRegularForm(self) -> bool:
        return self.suit.isRegularForm()

    def hasAtamaConnectedShuntsuPattern(self) -> bool:
        return self.waiting.isSendable() and self.suit.sum() >= 5 and self.suit.sum() <= 8

    def getWaitingTileCountWithAtama(self) -> int:
        return self.waiting.getWaitingTileCount() + ((2 if self.isAtamaConnectedShuntsu else 1) if self.waiting.isSendable else 0)

    def isIrreducible(self) -> bool:
        def isFormIrreducible(self, suits: list[Suit], isAtamaConnectedShuntsu: bool):
            for suit in suits:
                removedHand = Hand(suit, isAtamaConnectedShuntsu)

                if not (removedHand < self):
                    return False
            else:
                return True

        if not isFormIrreducible(self, Remove.getRemovedMentsuPatterns(self.suit), False):
            return False

        # 正規形のときは待ち送り形の既約もみる
        if self.isRegularForm():
            if not isFormIrreducible(self, Remove.getRemovedAtamaPatterns(self.suit), False) or not isFormIrreducible(self, Remove.getRemovedAtamaConnectedShuntsuPatterns(self.suit), True):
                return False

        return True

    def __lt__(self, other) -> bool:
        # あがり牌に昇格した場合(和了牌だが4枚使いだった場合)は待ちに関係する
        for (a, b) in zip(self.waiting.waitingCount, other.waiting.waitingCount):
            if a >= 1 and b == 0:
                return True

        return self.getWaitingTileCountWithAtama() != other.getWaitingTileCountWithAtama()
