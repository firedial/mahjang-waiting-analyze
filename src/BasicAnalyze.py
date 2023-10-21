from src.util.Suit import Suit
from src.util.WaitingStructure import WaitingStructure


def getTempaiCount(suits, num: int) -> int:
    tempaiCount = 0
    for suit, waitingStructure in suits.items():
        if suit.sum() != num:
            continue

        for tile, waitingType in zip(suit.suit, waitingStructure.waitingStructures):
            if tile < suit.MAX_TILE_COUNT and waitingType.hasWaiting():
                tempaiCount += 1
                break

    return tempaiCount


def main(records):
    suits = {}
    for record in records:
        suits[Suit(record['suit'])] = WaitingStructure.getWaitingStructureFromString(record['waitingStructure'])

    nums = [1, 2, 4, 5, 7, 8, 10, 11, 13]
    for num in nums:
        print(num, getTempaiCount(suits, num))
