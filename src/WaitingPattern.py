from src.Hand import Hand
import src.SuitLoop as SuitLoop


def setWaitingPatern(waitingPattern: dict, waitingNumber: int, suit):
    waitingPattern[tuple(suit.suit)] = {"suit": suit.suit, "number": waitingNumber, "length": suit.getRange(), "position": suit.getPosition(), "gravity": suit.getSuitGravityPosition()}


def getWaitingPattern(waitingPattern: dict, number: int):
    suit = SuitLoop.getFirstSuit(number)
    firstSuit = suit

    count = 0
    while (suit := SuitLoop.nextSuit(suit)) != firstSuit:
        count += 1
        waitingNumber = count * 100 + number

        # 基本形ではない時は考慮外
        if not suit.isBasicForm():
            continue

        # 範囲が8の時は両接地を考える
        if suit.getRange() == 8:
            # 右接地パターン
            hand = Hand(suit)
            if hand.isTempai() and hand.isIrreducible():
                setWaitingPatern(waitingPattern, waitingNumber, suit)
                setWaitingPatern(waitingPattern, waitingNumber, suit.getReverseSuit())

            # 左接地パターン
            leftAtattchSuit = suit.getOneLeftSuit()
            hand = Hand(leftAtattchSuit)
            if hand.isTempai() and hand.isIrreducible():
                setWaitingPatern(waitingPattern, waitingNumber, leftAtattchSuit)
                setWaitingPatern(waitingPattern, waitingNumber, leftAtattchSuit.getReverseSuit())
            continue

        # 聴牌形、既約系でなければ考慮外
        hand = Hand(suit)
        if not (hand.isTempai() and hand.isIrreducible()):
            continue

        # 範囲が9の時はその形だけを登録
        if suit.getRange() == 9:
            setWaitingPatern(waitingPattern, waitingNumber, suit)
            setWaitingPatern(waitingPattern, waitingNumber, suit.getReverseSuit())
            continue

        # 範囲が7以下のときは、移動系と右接地と左接地について見る
        # 移動形は無条件で登録
        setSuit = suit.getOneLeftSuit()
        for _ in range(8 - suit.getRange()):
            setSuit = setSuit.getOneRightSuit()
            setWaitingPatern(waitingPattern, waitingNumber, setSuit)
            setWaitingPatern(waitingPattern, waitingNumber, setSuit.getReverseSuit())

            continue

        # 範囲が7以下のときは、移動系と右接地と左接地について見る
        # 移動形は無条件で登録
        setSuit = suit.getOneLeftSuit()
        for _ in range(8 - suit.getRange()):
            setSuit = setSuit.getOneRightSuit()
            setWaitingPatern(waitingPattern, waitingNumber, setSuit)
            setWaitingPatern(waitingPattern, waitingNumber, setSuit.getReverseSuit())

        # 左接地は聴牌形で既約形かどうかをみる
        leftAtattchSuit = suit.getOneLeftSuit()
        hand = Hand(leftAtattchSuit)
        if hand.isTempai() and hand.isIrreducible():
            setWaitingPatern(waitingPattern, waitingNumber, leftAtattchSuit)
            setWaitingPatern(waitingPattern, waitingNumber, leftAtattchSuit.getReverseSuit())

        # 右接地も聴牌形で既約形かどうかをみる
        rightAttachSuit = suit.getRightAttachSuit()
        hand = Hand(rightAttachSuit)
        if hand.isTempai() and hand.isIrreducible():
            setWaitingPatern(waitingPattern, waitingNumber, rightAttachSuit)
            setWaitingPatern(waitingPattern, waitingNumber, rightAttachSuit.getReverseSuit())

    return waitingPattern

def main():
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

    return waitingPattern

