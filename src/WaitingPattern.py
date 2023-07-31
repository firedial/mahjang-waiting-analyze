from src.Hand import Hand
import src.SuitLoop as SuitLoop


def getWaitingPatterns(waitingPatterns: list, number: int):
    suit = SuitLoop.getFirstSuit(number)
    firstSuit = suit

    while True:
        # 基本形ではない時は考慮外
        if not suit.isBasicForm():
            suit = SuitLoop.nextSuit(suit)
            if suit == firstSuit:
                break

            continue

        # 範囲が8の時は両接地を考える
        if suit.getRange() == 8:
            # 右接地パターン
            rightAttachHand = Hand(suit)
            isRightIrreducible = rightAttachHand.isTempai() and rightAttachHand.isIrreducible()

            # 左接地パターン
            leftAttachHand = Hand(suit.getOneLeftSuit())
            isLeftIrreducible = leftAttachHand.isTempai() and leftAttachHand.isIrreducible()

            if isRightIrreducible or isLeftIrreducible:
                waitingPatterns.append({"suit": suit.suit, "right": isRightIrreducible, "left": isLeftIrreducible, "isACS": False})
                # 雀頭接続順子のパターンの考慮
                if rightAttachHand.hasAtamaConnectedShuntsuPattern():
                    waitingPatterns.append({"suit": suit.suit, "right": isRightIrreducible, "left": isLeftIrreducible, "isACS": True})


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
            waitingPatterns.append({"suit": suit.suit, "right": True, "left": True, "isACS": False})
            # 雀頭接続順子のパターンの考慮
            if rightAttachHand.hasAtamaConnectedShuntsuPattern():
                waitingPatterns.append({"suit": suit.suit, "right": True, "left": True, "isACS": True})

            suit = SuitLoop.nextSuit(suit)
            if suit == firstSuit:
                break

            continue

        # 範囲が7以下のときは、移動系と右接地と左接地について見る
        # 右接地パターン
        rightAttachHand = Hand(suit.getRightAttachSuit())
        isRightIrreducible = rightAttachHand.isTempai() and rightAttachHand.isIrreducible()

        # 左接地パターン
        leftAttachHand = Hand(suit.getOneLeftSuit())
        isLeftIrreducible = leftAttachHand.isTempai() and leftAttachHand.isIrreducible()

        waitingPatterns.append({"suit": suit.suit, "right": isRightIrreducible, "left": isLeftIrreducible, "isACS": False})
        # 雀頭接続順子のパターンの考慮
        if rightAttachHand.hasAtamaConnectedShuntsuPattern():
            waitingPatterns.append({"suit": suit.suit, "right": isRightIrreducible, "left": isLeftIrreducible, "isACS": True})

        suit = SuitLoop.nextSuit(suit)
        if suit == firstSuit:
            break

def main():
    waitingPatterns = []
    getWaitingPatterns(waitingPatterns, 1)
    getWaitingPatterns(waitingPatterns, 2)
    getWaitingPatterns(waitingPatterns, 4)
    getWaitingPatterns(waitingPatterns, 5)
    getWaitingPatterns(waitingPatterns, 7)
    getWaitingPatterns(waitingPatterns, 8)
    getWaitingPatterns(waitingPatterns, 10)
    getWaitingPatterns(waitingPatterns, 11)
    getWaitingPatterns(waitingPatterns, 13)

    return waitingPatterns

