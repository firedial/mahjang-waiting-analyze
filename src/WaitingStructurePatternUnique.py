import src.util.SuitLoop as SuitLoop


def getWaitingPatternsLoop(waitingStructurePossiblePatterns: list, waitingStructurePatterns: dict, number: int):
    suit = SuitLoop.getFirstSuit(number)
    firstSuit = suit

    while True:
        waitingStructurePossiblePattern = []
        suit.getWaitingStructurePossiblePattern(suit, waitingStructurePatterns, waitingStructurePossiblePattern)
        waitingStructurePossiblePattern = set(waitingStructurePossiblePattern)

        if len(waitingStructurePossiblePattern) == 0:
            RuntimeError("0 is invalid")

        if waitingStructurePossiblePattern == set({2, 11}):
            waitingStructurePossiblePattern = set({11})

        elif len(waitingStructurePossiblePattern) > 1:
            waitingStructurePossiblePatterns.append({"suit": suit.suit, "pattern": waitingStructurePossiblePattern})

        suit = SuitLoop.nextSuit(suit)
        if suit == firstSuit:
            break


def main(waitingStructurePatterns, tileCounts):
    waitingStructurePossiblePatterns = []

    for tileCount in tileCounts:
        getWaitingPatternsLoop(waitingStructurePossiblePatterns, waitingStructurePatterns, tileCount)

    return waitingStructurePossiblePatterns
