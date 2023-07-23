from src.Hand import Hand
from src.Waiting import Waiting
import src.Remove as Remove
import src.Agari as Agari


def isMentsuIrreducible(hand: Hand) -> bool:
    removedSuits = Remove.getRemovedMentsuPatterns(hand.suit)

    for removedSuits in removedSuits:
        removedHand = Hand(removedSuits, False)

        if not (removedHand < hand):
            return False
    else:
        return True


def isAtamaIrreducible(hand: Hand) -> bool:
    removedSuits = Remove.getRemovedAtamaPatterns(hand.suit)

    for removedSuits in removedSuits:
        removedHand = Hand(removedSuits, False)

        if not (removedHand < hand):
            return False
    else:
        return True


def isAtamaConnectedShuntsuIrreducible(hand: Hand) -> bool:
    removedSuits = Remove.getRemovedAtamaConnectedShuntsuPatterns(hand.suit)

    for removedSuits in removedSuits:
        removedHand = Hand(removedSuits, True)

        if not (removedHand < hand):
            return False
    else:
        return True


def isIrreducible(hand: Hand):
    if not isMentsuIrreducible(hand):
        return False

    # 正規形のときは待ち送り形の既約もみる
    if hand.isRegularForm():
        if not isAtamaIrreducible(hand) or not isAtamaConnectedShuntsuIrreducible(hand):
            return False

    return True

