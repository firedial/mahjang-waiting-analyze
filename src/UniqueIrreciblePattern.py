from src.Hand import Hand
from src.Suit import Suit
import src.Remove as Remove
import src.SuitLoop as SuitLoop
import result.waitingPattern
from src.WaitingPatternUtil import WaitingPatternUtil
import csv


def getIrreducibles(hand: Hand, waitingPatternUtil: WaitingPatternUtil):
    waitingNumber = waitingPatternUtil.getWaitingPatternNumber(hand)
    if waitingNumber is not None:
        return set([waitingNumber])

    result = set()
    if not hand.isTempai():
        return result

    if hand.suit.isRegularForm() and hand.suit.sum() >= 10:
        suits = Remove.getRemovedAtamaConnectedShuntsuPatterns(hand.suit)
        for checkSuit in suits:
            checkHand = Hand(checkSuit, True)
            if checkHand == hand:
                result |= getIrreducibles(checkHand, waitingPatternUtil)

    if hand.suit.isRegularForm():
        suits = Remove.getRemovedAtamaPatterns(hand.suit)
        for checkSuit in suits:
            checkHand = Hand(checkSuit, hand.isAtamaConnectedShuntsu)
            if checkHand == hand:
                result |= getIrreducibles(checkHand, waitingPatternUtil)

    suits = Remove.getRemovedMentsuPatterns(hand.suit)
    for checkSuit in suits:
        checkHand = Hand(checkSuit, hand.isAtamaConnectedShuntsu)
        if checkHand == hand:
            result |= getIrreducibles(checkHand, waitingPatternUtil)

    return result


def checkIrrecible(number: int):
    suit = SuitLoop.getFirstSuit(number)
    firstSuit = suit

    irreducibleWaitings = {}
    while True:
        irreducibles = getIrreducibles(Hand(suit), WaitingPatternUtil())
        if len(irreducibles) > 0:
            irreducibleWaitings[suit.suit] = irreducibles

        suit = SuitLoop.nextSuit(suit)
        if suit == firstSuit:
            break

    return irreducibleWaitings


def main():
    irreducibleWaitings = {}
    irreducibleWaitings |= checkIrrecible(1)
    irreducibleWaitings |= checkIrrecible(2)
    irreducibleWaitings |= checkIrrecible(4)
    irreducibleWaitings |= checkIrrecible(5)
    irreducibleWaitings |= checkIrrecible(7)
    irreducibleWaitings |= checkIrrecible(8)
    irreducibleWaitings |= checkIrrecible(10)
    irreducibleWaitings |= checkIrrecible(11)
    irreducibleWaitings |= checkIrrecible(13)

    return irreducibleWaitings