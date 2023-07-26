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


def setWaitingPatern(waitingPattern: dict, waitingNumber: int, suit):
    waitingPattern[tuple(suit.suit)] = {"number": waitingNumber, "length": suit.getRange(), "position": suit.getPosition(), "gravity": suit.getSuitGravityPosition()}


def getWaitingPattern(waitingPattern: dict, number: int):
    suit = getSuitFromNumber(number)
    firstSuit = suit.suit.copy()

    count = 0
    while True:
        count += 1
        waitingNumber = count * 100 + number
        if not suit.isBasicForm():
            suit = SuitLoop.nextSuit(suit)
            if suit.suit == firstSuit:
                break

            continue

        hand = Hand.Hand(suit, False)
        if not (hand.isBasicForm() and hand.isTempai() and hand.isIrreducible()):
            suit = SuitLoop.nextSuit(suit)
            if suit.suit == firstSuit:
                break

            continue

        if suit.getRange() > 7:
            setWaitingPatern(waitingPattern, waitingNumber, suit)
            setWaitingPatern(waitingPattern, waitingNumber, suit.getReverseSuit())

            suit = SuitLoop.nextSuit(suit)
            if suit.suit == firstSuit:
                break

            continue

        setSuit = suit.getOneLeftSuit()
        for index in range(8 - suit.getRange()):
            setSuit = setSuit.getOneRightSuit()
            setWaitingPatern(waitingPattern, waitingNumber, setSuit)
            setWaitingPatern(waitingPattern, waitingNumber, setSuit.getReverseSuit())

        leftAtattchSuit = suit.getOneLeftSuit()
        hand = Hand.Hand(leftAtattchSuit, False)
        if hand.isTempai() and hand.isIrreducible():
            setWaitingPatern(waitingPattern, waitingNumber, leftAtattchSuit)
            setWaitingPatern(waitingPattern, waitingNumber, leftAtattchSuit.getReverseSuit())

        rightAttachSuit = suit.getRightAttachSuit()
        hand = Hand.Hand(rightAttachSuit, False)
        if hand.isTempai() and hand.isIrreducible():
            setWaitingPatern(waitingPattern, waitingNumber, rightAttachSuit)
            setWaitingPatern(waitingPattern, waitingNumber, rightAttachSuit.getReverseSuit())

        suit = SuitLoop.nextSuit(suit)
        if suit.suit == firstSuit:
            break

    return waitingPattern


waitingPattern = {}
getWaitingPattern(waitingPattern, 1)
getWaitingPattern(waitingPattern, 2)
getWaitingPattern(waitingPattern, 4)
getWaitingPattern(waitingPattern, 5)
getWaitingPattern(waitingPattern, 7)
getWaitingPattern(waitingPattern, 8)
getWaitingPattern(waitingPattern, 10)
getWaitingPattern(waitingPattern, 11)
getWaitingPattern(waitingPattern, 13)

print(waitingPattern)
print(len(waitingPattern))
