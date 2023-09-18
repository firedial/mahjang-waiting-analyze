from src.util.Suit import Suit
import src.util.SuitLoop as SuitLoop
from src.util.WaitingStructure import WaitingStructure


def setWaitingNumber(waitingPatterns: list) -> list:
    sortedPatterns = sorted(waitingPatterns, key = lambda x: x['suitNumber'], reverse = True)
    for pattern in sortedPatterns:
        pattern.pop("suitNumber")

    return sortedPatterns


def getWaitingStructureString(waitingStructure: WaitingStructure) -> str:
    string = ''

    for waitingType in waitingStructure.waitingStructures:
        string += waitingType.getWaitingTypeString()

    return "|" + string[0:3] + "|" + string[3:6] + "|" + string[6:] + "|"


def getWaitingPatterns(suit: Suit):
    # 基本形かつ聴牌形ではない時は考慮外
    if not suit.isBasicForm() or not suit.isTempaiWithoutTileCount():
        return None

    return {"suit": suit.getLeftAttachSuit().suit, "waitingStructure": getWaitingStructureString(suit.getLeftAttachSuit().waitingStructure), "suitNumber": suit.getSuitNumber()}


def getWaitingPatternsLoop(waitingPatterns: list, number: int):
    suit = SuitLoop.getFirstSuit(number)
    firstSuit = suit

    while True:
        waitingPattern = getWaitingPatterns(suit)
        if waitingPattern is not None:
            waitingPatterns.append(waitingPattern)

        suit = SuitLoop.nextSuit(suit)
        if suit == firstSuit:
            break


def main():
    waitingPatterns = []
    getWaitingPatternsLoop(waitingPatterns, 1)
    getWaitingPatternsLoop(waitingPatterns, 2)
    getWaitingPatternsLoop(waitingPatterns, 4)
    getWaitingPatternsLoop(waitingPatterns, 5)
    getWaitingPatternsLoop(waitingPatterns, 7)
    getWaitingPatternsLoop(waitingPatterns, 8)
    getWaitingPatternsLoop(waitingPatterns, 10)
    getWaitingPatternsLoop(waitingPatterns, 11)
    getWaitingPatternsLoop(waitingPatterns, 13)
    return setWaitingNumber(waitingPatterns)
