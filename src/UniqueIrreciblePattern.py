from src.Hand import Hand
from src.Suit import Suit
import src.Remove as Remove
import src.SuitLoop as SuitLoop
import result.waitingPattern

def getWaitingPatterns() -> dict:
    waitingPatterns = {}
    for waiting in result.waitingPattern.getWaitingPatterns():
        waitingPatterns[waiting["suit"]] = waiting

    return waitingPatterns

def getIrreducibles(suit: Suit, waitingPatterns: dict):
    if suit.suit in waitingPatterns:
        return set((suit.suit, ))

    hand = Hand(suit, False)
    result = set()

    if not hand.isTempai():
        return result

    if suit.isRegularForm() and suit.sum() >= 10:
        suits = Remove.getRemovedAtamaConnectedShuntsuPatterns(suit)
        for checkSuit in suits:
            checkHand = Hand(checkSuit, False)
            if not checkHand < hand:
                result |= getIrreducibles(checkSuit, waitingPatterns)

    if suit.isRegularForm():
        suits = Remove.getRemovedAtamaPatterns(suit)
        for checkSuit in suits:
            checkHand = Hand(checkSuit, False)
            if not checkHand < hand:
                result |= getIrreducibles(checkSuit, waitingPatterns)

    suits = Remove.getRemovedMentsuPatterns(suit)
    for checkSuit in suits:
        checkHand = Hand(checkSuit, False)
        if not checkHand < hand:
            result |= getIrreducibles(checkSuit, waitingPatterns)

    return result


def checkIrrecible(number: int):
    suit = SuitLoop.getFirstSuit(number)
    firstSuit = suit

    waitingPatterns = getWaitingPatterns()
    irreducibleWaitings = {}

    while (suit := SuitLoop.nextSuit(suit)) != firstSuit:
        irreducibles = getIrreducibles(suit, waitingPatterns)
        if len(set(map(lambda x: waitingPatterns[x]['number'], irreducibles))) > 1:
            irreducibleWaitings[suit.suit] = irreducibles

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