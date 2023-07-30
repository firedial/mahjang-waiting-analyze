from src.Hand import Hand
import src.SuitLoop as SuitLoop


def setWaitingPatern(waitingPatterns: dict, waitingNumber: int, suit):
    waitingPatterns[tuple(suit.suit)] = {"suit": suit.suit, "number": waitingNumber, "position": suit.getPosition(), "gravity": suit.getSuitGravityPosition()}


def getWaitingPattern(waitingPatterns: dict, number: int):
    suit = SuitLoop.getFirstSuit(number)
    firstSuit = suit

    count = -1
    while True:
        count += 1
        waitingNumber = count * 100 + number

        # 基本形ではない時は考慮外
        if not suit.isBasicForm():
            suit = SuitLoop.nextSuit(suit)
            if suit == firstSuit:
                break

            continue

        # 範囲が8の時は両接地を考える
        if suit.getRange() == 8:
            # 右接地パターン
            hand = Hand(suit)
            if hand.isTempai() and hand.isIrreducible():
                setWaitingPatern(waitingPatterns, waitingNumber, suit)
                setWaitingPatern(waitingPatterns, waitingNumber, suit.getReverseSuit())

            # 左接地パターン
            leftAtattchSuit = suit.getOneLeftSuit()
            hand = Hand(leftAtattchSuit)
            if hand.isTempai() and hand.isIrreducible():
                setWaitingPatern(waitingPatterns, waitingNumber, leftAtattchSuit)
                setWaitingPatern(waitingPatterns, waitingNumber, leftAtattchSuit.getReverseSuit())

            suit = SuitLoop.nextSuit(suit)
            if suit == firstSuit:
                break

            continue

        # 聴牌形、既約系でなければ考慮外
        hand = Hand(suit)
        if not (hand.isTempai() and hand.isIrreducible()):
            suit = SuitLoop.nextSuit(suit)
            if suit == firstSuit:
                break

            continue

        # 範囲が9の時はその形だけを登録
        if suit.getRange() == 9:
            setWaitingPatern(waitingPatterns, waitingNumber, suit)
            setWaitingPatern(waitingPatterns, waitingNumber, suit.getReverseSuit())
            suit = SuitLoop.nextSuit(suit)
            if suit == firstSuit:
                break

            continue

        # 範囲が7以下のときは、移動系と右接地と左接地について見る
        # 移動形は無条件で登録
        setSuit = suit.getOneLeftSuit()
        for _ in range(8 - suit.getRange()):
            setSuit = setSuit.getOneRightSuit()
            setWaitingPatern(waitingPatterns, waitingNumber, setSuit)
            setWaitingPatern(waitingPatterns, waitingNumber, setSuit.getReverseSuit())

        # 左接地は聴牌形で既約形かどうかをみる
        leftAtattchSuit = suit.getOneLeftSuit()
        hand = Hand(leftAtattchSuit)
        if hand.isTempai() and hand.isIrreducible():
            setWaitingPatern(waitingPatterns, waitingNumber, leftAtattchSuit)
            setWaitingPatern(waitingPatterns, waitingNumber, leftAtattchSuit.getReverseSuit())

        # 右接地も聴牌形で既約形かどうかをみる
        rightAttachSuit = suit.getRightAttachSuit()
        hand = Hand(rightAttachSuit)
        if hand.isTempai() and hand.isIrreducible():
            setWaitingPatern(waitingPatterns, waitingNumber, rightAttachSuit)
            setWaitingPatern(waitingPatterns, waitingNumber, rightAttachSuit.getReverseSuit())

        suit = SuitLoop.nextSuit(suit)
        if suit == firstSuit:
            break

def main():
    waitingPatterns = {}
    getWaitingPattern(waitingPatterns, 1)
    getWaitingPattern(waitingPatterns, 2)
    getWaitingPattern(waitingPatterns, 4)
    getWaitingPattern(waitingPatterns, 5)
    getWaitingPattern(waitingPatterns, 7)
    getWaitingPattern(waitingPatterns, 8)
    getWaitingPattern(waitingPatterns, 10)
    getWaitingPattern(waitingPatterns, 11)
    getWaitingPattern(waitingPatterns, 13)

    return waitingPatterns

