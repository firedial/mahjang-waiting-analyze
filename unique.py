import src.Hand as Hand
import src.Suit as Suit
import src.Block as Block
import src.Remove as Remove
import src.Agari as Agari
import src.SuitLoop as SuitLoop


def getSuitFromNumber(number: int) -> Suit:
    match number:
        case 1:
            return Suit.Suit([0, 0, 0, 0, 0, 0, 0, 0, 1])
        case 2:
            return Suit.Suit([0, 0, 0, 0, 0, 0, 0, 0, 2])
        case 4:
            return Suit.Suit([0, 0, 0, 0, 0, 0, 0, 0, 4])
        case 5:
            return Suit.Suit([0, 0, 0, 0, 0, 0, 0, 1, 4])
        case 7:
            return Suit.Suit([0, 0, 0, 0, 0, 0, 0, 3, 4])
        case 8:
            return Suit.Suit([0, 0, 0, 0, 0, 0, 0, 4, 4])
        case 10:
            return Suit.Suit([0, 0, 0, 0, 0, 0, 2, 4, 4])
        case 11:
            return Suit.Suit([0, 0, 0, 0, 0, 0, 3, 4, 4])
        case 13:
            return Suit.Suit([0, 0, 0, 0, 0, 1, 4, 4, 4])


def getWaitingPattern(number: int):
    suit = getSuitFromNumber(number)
    firstSuit = suit.suit.copy()
    waitingPattern = set()
    while True:
        if not suit.isBasicForm():
            suit = SuitLoop.nextSuit(suit)
            if (suit.suit == firstSuit):
                break

            continue

        hand = Hand.Hand(suit, False)
        if hand.isBasicForm() and hand.isTempai() and hand.isIrreducible():
            reverseRightAtattchSuit = suit.getOneLeftSuit().getReverseSuit()

            if suit.getRange() <= 7:
                for _ in range(8 - suit.getRange()):
                    reverseRightAtattchSuit = reverseRightAtattchSuit.getOneLeftSuit()
                    waitingPattern.add(tuple(reverseRightAtattchSuit.suit))
                    waitingPattern.add(tuple(reverseRightAtattchSuit.getReverseSuit().suit))

                leftAtattchSuit = suit.getOneLeftSuit()
                hand = Hand.Hand(leftAtattchSuit, False)
                if hand.isTempai() and hand.isIrreducible():
                    waitingPattern.add(tuple(leftAtattchSuit.suit))
                    waitingPattern.add(tuple(leftAtattchSuit.getReverseSuit().suit))

                rightAttachSuit = suit.getRightAttachSuit()
                hand = Hand.Hand(rightAttachSuit, False)
                if hand.isTempai() and hand.isIrreducible():
                    waitingPattern.add(tuple(rightAttachSuit.suit))
                    waitingPattern.add(tuple(rightAttachSuit.getReverseSuit().suit))
            else:
                waitingPattern.add(tuple(suit.suit))
                waitingPattern.add(tuple(suit.getReverseSuit().suit))

        suit = SuitLoop.nextSuit(suit)
        if (suit.suit == firstSuit):
            break

    return waitingPattern

waitingPattern = set()
waitingPattern |= getWaitingPattern(1)
waitingPattern |= getWaitingPattern(2)
waitingPattern |= getWaitingPattern(4)
waitingPattern |= getWaitingPattern(5)
waitingPattern |= getWaitingPattern(7)
waitingPattern |= getWaitingPattern(8)
waitingPattern |= getWaitingPattern(10)
waitingPattern |= getWaitingPattern(11)
waitingPattern |= getWaitingPattern(13)

for t in waitingPattern:
    print(t)
print(len(waitingPattern))
