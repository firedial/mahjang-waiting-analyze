from src.Hand import Hand
from src.Suit import Suit
import src.Remove as Remove
import src.SuitLoop as SuitLoop
import result.waitingPattern

def getAllWaitingPatterns() -> dict:
    waitingPatterns = result.waitingPattern.getWaitingPatterns()
    allWaitingPatterns = {}
    for waitingPattern in waitingPatterns:
        suit = Suit(waitingPattern["suit"])

        if suit.getRange() == 9:
            allWaitingPatterns[(suit.suit, waitingPattern["isAcs"])] = {"suit": suit.suit, "isAcs": waitingPattern["isAcs"], "number": waitingPattern["number"]}
            allWaitingPatterns[(suit.getReverseSuit().suit, waitingPattern["isAcs"])] = {"suit": suit.getReverseSuit().suit, "isAcs": waitingPattern["isAcs"], "number": waitingPattern["number"]}
        elif suit.getRange() == 8:
            if waitingPattern["right"]:
                allWaitingPatterns[(suit.suit, waitingPattern["isAcs"])] = {"suit": suit.suit, "isAcs": waitingPattern["isAcs"], "number": waitingPattern["number"]}
                allWaitingPatterns[(suit.getReverseSuit().suit, waitingPattern["isAcs"])] = {"suit": suit.getReverseSuit().suit, "isAcs": waitingPattern["isAcs"], "number": waitingPattern["number"]}
            if waitingPattern["left"]:
                suit = suit.getOneLeftSuit()
                allWaitingPatterns[(suit.suit, waitingPattern["isAcs"])] = {"suit": suit.suit, "isAcs": waitingPattern["isAcs"], "number": waitingPattern["number"]}
                allWaitingPatterns[(suit.getReverseSuit().suit, waitingPattern["isAcs"])] = {"suit": suit.getReverseSuit().suit, "isAcs": waitingPattern["isAcs"], "number": waitingPattern["number"]}
        else:
            suit = suit.getOneLeftSuit()
            if waitingPattern["left"]:
                allWaitingPatterns[(suit.suit, waitingPattern["isAcs"])] = {"suit": suit.suit, "isAcs": waitingPattern["isAcs"], "number": waitingPattern["number"]}
                allWaitingPatterns[(suit.getReverseSuit().suit, waitingPattern["isAcs"])] = {"suit": suit.getReverseSuit().suit, "isAcs": waitingPattern["isAcs"], "number": waitingPattern["number"]}

            for _ in range(8 - suit.getRange()):
                suit = suit.getOneRightSuit()
                allWaitingPatterns[(suit.suit, waitingPattern["isAcs"])] = {"suit": suit.suit, "isAcs": waitingPattern["isAcs"], "number": waitingPattern["number"]}
                allWaitingPatterns[(suit.getReverseSuit().suit, waitingPattern["isAcs"])] = {"suit": suit.getReverseSuit().suit, "isAcs": waitingPattern["isAcs"], "number": waitingPattern["number"]}

            suit = suit.getOneRightSuit()
            if waitingPattern["right"]:
                allWaitingPatterns[(suit.suit, waitingPattern["isAcs"])] = {"suit": suit.suit, "isAcs": waitingPattern["isAcs"], "number": waitingPattern["number"]}
                allWaitingPatterns[(suit.getReverseSuit().suit, waitingPattern["isAcs"])] = {"suit": suit.getReverseSuit().suit, "isAcs": waitingPattern["isAcs"], "number": waitingPattern["number"]}

    return allWaitingPatterns

def getIrreducibles(suit: Suit, allWaitingPatterns: dict):
    if (suit.suit, False) in allWaitingPatterns:
        t = tuple((suit.suit, False))
        s = set()
        s.add(t)
        return s

    hand = Hand(suit, False)
    result = set()

    if not hand.isTempai():
        return result

    if suit.isRegularForm() and suit.sum() >= 10:
        suits = Remove.getRemovedAtamaConnectedShuntsuPatterns(suit)
        for checkSuit in suits:
            checkHand = Hand(checkSuit, True)
            if not checkHand < hand:
                result |= getIrreducibles(checkSuit, allWaitingPatterns)

    if suit.isRegularForm():
        suits = Remove.getRemovedAtamaPatterns(suit)
        for checkSuit in suits:
            checkHand = Hand(checkSuit)
            if not checkHand < hand:
                result |= getIrreducibles(checkSuit, allWaitingPatterns)

    suits = Remove.getRemovedMentsuPatterns(suit)
    for checkSuit in suits:
        checkHand = Hand(checkSuit)
        if not checkHand < hand:
            result |= getIrreducibles(checkSuit, allWaitingPatterns)

    return result


def checkIrrecible(number: int):
    suit = SuitLoop.getFirstSuit(number)
    firstSuit = suit

    allWaitingPatterns = getAllWaitingPatterns()
    irreducibleWaitings = {}

    while True:
        irreducibles = getIrreducibles(suit, allWaitingPatterns)
        if len(set(map(lambda x: allWaitingPatterns[x]['number'], irreducibles))) > 0:
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