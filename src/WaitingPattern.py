from src.util.Suit import Suit
import src.util.SuitLoop as SuitLoop


def setWaitingNumber(waitingPatterns: list) -> list:
    sortedPatterns = sorted(waitingPatterns, key = lambda x: x['suitNumber'], reverse = True)
    count = 0
    for pattern in sortedPatterns:
        count += 1
        pattern["number"] = f"W{count:03}"
        pattern.pop("suitNumber")

    return sortedPatterns


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

        if suit.isRangeFull():
            # 聴牌形、既約系でなければ考慮外
            if not (suit.isTempai() and suit.isIrreducible()):
                suit = SuitLoop.nextSuit(suit)
                if suit == firstSuit:
                    break

                continue

            isRightIrreducible = True
            isLeftIrreducible = True

        elif suit.hasOneRoomRange():
            # 右接地パターン
            rightAttachSuit = suit
            isRightIrreducible = rightAttachSuit.isTempai() and rightAttachSuit.isIrreducible()

            # 左接地パターン
            leftAttachSuit = suit.getLeftAttachSuit()
            isLeftIrreducible = leftAttachSuit.isTempai() and leftAttachSuit.isIrreducible()

            # どっちに接地していても既約でない場合は登録しない
            if (not isRightIrreducible) and (not isLeftIrreducible):
                suit = SuitLoop.nextSuit(suit)
                if suit == firstSuit:
                    break

                continue

        else:
            # 範囲が7以下のときは、移動系と右接地と左接地について見る

            # 無接地パターン
            isCenterIrreducible = suit.isTempai() and suit.isIrreducible()

            # 右接地パターン
            rightAttachSuit = suit.getRightAttachSuit()
            isRightIrreducible = rightAttachSuit.isTempai() and rightAttachSuit.isIrreducible()

            # 左接地パターン
            leftAttachSuit = suit.getLeftAttachSuit()
            isLeftIrreducible = leftAttachSuit.isTempai() and leftAttachSuit.isIrreducible()

            # 無接地は既約じゃないが、接地パターンが既約になる場合はない想定
            if not isCenterIrreducible and (isRightIrreducible or isLeftIrreducible):
                raise RuntimeError("Unexpected error.")

            # 既約でない場合は登録しない
            if not isCenterIrreducible:
                suit = SuitLoop.nextSuit(suit)
                if suit == firstSuit:
                    break

                continue

        waitingPatterns.append({"suit": suit.suit, "left": isLeftIrreducible, "right": isRightIrreducible, "isSendable": suit.isSendable(), "suitNumber": 1})

        suit = SuitLoop.nextSuit(suit)
        if suit == firstSuit:
            break


def main():
    isSameWaiting = lambda x: True
    waitingPatterns = []
    getWaitingPatterns(waitingPatterns, 1)
    getWaitingPatterns(waitingPatterns, 2)
    getWaitingPatterns(waitingPatterns, 4)
    getWaitingPatterns(waitingPatterns, 5)
    getWaitingPatterns(waitingPatterns, 7)
    return setWaitingNumber(waitingPatterns)
    getWaitingPatterns(waitingPatterns, 8)
    getWaitingPatterns(waitingPatterns, 10)
    getWaitingPatterns(waitingPatterns, 11)
    getWaitingPatterns(waitingPatterns, 13)
    return setWaitingNumber(waitingPatterns)
