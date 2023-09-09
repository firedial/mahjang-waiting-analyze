from dataclasses import dataclass
from src.Suit import Suit
from src.Waiting import Waiting
import src.Remove as Remove
import src.Agari as Agari
from functools import cached_property


@dataclass(frozen=True)
class Hand:

    suit: Suit
    isAtamaConnectedShuntsu: bool

    def __init__(self, suit: Suit, isAtamaConnectedShuntsu: bool = False):
        object.__setattr__(self, "suit", suit)
        object.__setattr__(self, "isAtamaConnectedShuntsu", isAtamaConnectedShuntsu)

    @cached_property
    def waiting(self) -> Waiting:
        return Agari.getWaiting(self.suit)

    @cached_property
    def isSendable(self) -> bool:
        return Agari.isAgari(self.suit)

    def isTempai(self) -> bool:
        return self.waiting.getWaitingTileCount() > 0 or self.isSendable

    def isRyanmen(self, index, isFormer) -> bool:
        return Agari.isRyanmen(self.suit, index, isFormer)

    def isBasicForm(self) -> bool:
        return self.suit.isBasicForm()

    def isRegularForm(self) -> bool:
        return self.suit.isRegularForm()

    def hasAtamaConnectedShuntsuPattern(self) -> bool:
        return self.isSendable and self.suit.sum() >= 5 and self.suit.sum() <= 8

    def isIrreducible(self) -> bool:
        def isFormIrreducible(self, suits: list[Suit], isAtamaConnectedShuntsu: bool):
            for suit in suits:
                removedHand = Hand(suit)

                if removedHand == self:
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

    def __eq__(self, other) -> bool:
        removedSuit = other.suit - self.suit

        # 面子だった場合は待ちが変わっていないことだけ見ればいい
        if removedSuit.sum() == 3:
            return self.waiting == other.waiting and self.isSendable == other.isSendable

        # 雀頭だった場合
        if removedSuit.sum() == 2:
            index2 = removedSuit.findFirstNumber(2)
            if self.isSendable and Agari.isShampon(other.suit, index2):
                if self.waiting.waitings[index2]:
                    return False
                addedWaiting = self.waiting.getWaitingAddTile(index2)
                return addedWaiting == other.waiting
            else:
                return self.waiting == other.waiting

        # 雀頭接続順子だった場合
        if removedSuit.sum() == 5:
            index3 = removedSuit.findFirstNumber(3)
            index1 = removedSuit.findFirstNumber(1)

            # 311 パターン
            if index3 < index1:
                if self.isSendable and Agari.isShampon(other.suit, index3) and Agari.isRyanmen(other.suit, index3, True) and Agari.isRyanmen(other.suit, index3 + 3, False):
                    if self.waiting.waitings[index1 + 2] and self.waiting.waitings[index3]:
                        return False
                    addedWaiting = self.waiting.getWaitingAddTile(index1 + 2).getWaitingAddTile(index3)
                    return addedWaiting == other.waiting
                else:
                    return self.waiting == other.waiting
            # 113 パターン
            else:
                if self.isSendable and Agari.isShampon(other.suit, index3) and Agari.isRyanmen(other.suit, index3, False) and Agari.isRyanmen(other.suit, index3 - 3, True):
                    if self.waiting.waitings[index1 - 1] and self.waiting.waitings[index3]:
                        return False
                    addedWaiting = self.waiting.getWaitingAddTile(index1 - 1).getWaitingAddTile(index3)
                    return addedWaiting == other.waiting
                else:
                    return self.waiting == other.waiting

        raise ValueError("Invalid pattern.")

    def __ne__(self, other) -> bool:
        return not (self == other)
