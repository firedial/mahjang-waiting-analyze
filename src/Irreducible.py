from src.Hand import Hand
from src.Waiting import Waiting
import src.Remove as Remove
import src.Agari as Agari


def isMentsuIrreducible(hand: Hand) -> bool:
    waiting: Waiting = Agari.getWaiting(hand)
    removedHands: list[Waiting] = Remove.getRemovedMentsuPatterns(hand)

    for removedHand in removedHands:
        removedHandWaiting = Agari.getWaiting(removedHand)

        if not (removedHandWaiting < waiting):
            return False
    else:
        return True


def isAtamaIrreducible(hand: Hand) -> bool:
    waiting: Waiting = Agari.getWaiting(hand)
    removedHands: list[Waiting] = Remove.getRemovedAtamaPatterns(hand)

    for removedHand in removedHands:
        removedHandWaiting = Agari.getWaiting(removedHand)

        if not (removedHandWaiting < waiting):
            return False
    else:
        return True


def isAtamaConnectedShuntsuIrreducible(hand: Hand) -> bool:
    waiting: Waiting = Agari.getWaiting(hand)
    removedHands: list[Waiting] = Remove.getRemovedAtamaPatterns(hand)

    for removedHand in removedHands:
        removedHandWaiting = Agari.getWaiting(removedHand, 2)

        if not (removedHandWaiting < waiting):
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

