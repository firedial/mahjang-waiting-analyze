from src.Hand import Hand
import src.SuitLoop as SuitLoop


def setWaitingNumber(waitingPatterns: list) -> list:
    sortedPatterns = sorted(waitingPatterns, key = lambda x: x['suitNumber'], reverse = True)
    count = 0
    for pattern in sortedPatterns:
        count += 1
        pattern["number"] = f"W{count:03}"
        pattern.pop("suitNumber")

    return sortedPatterns


def getWaitingPatterns(waitingPatterns: list, number: int, isSameWaiting):
    suit = SuitLoop.getFirstSuit(number)
    firstSuit = suit

    while True:
        # 基本形ではない時は考慮外
        if not suit.isBasicForm():
            suit = SuitLoop.nextSuit(suit)
            if suit == firstSuit:
                break

            continue

        if suit.getRange() == 9:
            # 聴牌形、既約系でなければ考慮外
            hand = Hand(suit)
            if not (hand.isTempai() and hand.isIrreducibleWithJudgeFunction(isSameWaiting)):
                suit = SuitLoop.nextSuit(suit)
                if suit == firstSuit:
                    break

                continue

            isRightIrreducible = True
            isLeftIrreducible = True

        elif suit.getRange() == 8:
            # 範囲が8の時は両接地を考える
            hand = Hand(suit)

            # 右接地パターン
            rightAttachHand = Hand(suit)
            isRightIrreducible = rightAttachHand.isTempai() and rightAttachHand.isIrreducibleWithJudgeFunction(isSameWaiting)

            # 左接地パターン
            leftAttachHand = Hand(suit.getOneLeftSuit())
            isLeftIrreducible = leftAttachHand.isTempai() and leftAttachHand.isIrreducibleWithJudgeFunction(isSameWaiting)

            # どっちに接地していても既約でない場合は登録しない
            if (not isRightIrreducible) and (not isLeftIrreducible):
                suit = SuitLoop.nextSuit(suit)
                if suit == firstSuit:
                    break

                continue

        else:
            # 範囲が7以下のときは、移動系と右接地と左接地について見る

            # 無接地パターン
            hand = Hand(suit)
            isCenterIrreducible = hand.isTempai() and hand.isIrreducibleWithJudgeFunction(isSameWaiting)

            # 右接地パターン
            rightAttachHand = Hand(suit.getRightAttachSuit())
            isRightIrreducible = rightAttachHand.isTempai() and rightAttachHand.isIrreducibleWithJudgeFunction(isSameWaiting)

            # 左接地パターン
            leftAttachHand = Hand(suit.getOneLeftSuit())
            isLeftIrreducible = leftAttachHand.isTempai() and leftAttachHand.isIrreducibleWithJudgeFunction(isSameWaiting)

            # 無接地は既約じゃないが、接地パターンが既約になる場合はない想定
            if not isCenterIrreducible and (isRightIrreducible or isLeftIrreducible):
                raise RuntimeError("Unexpected error.")

            # 既約でない場合は登録しない
            if not isCenterIrreducible:
                suit = SuitLoop.nextSuit(suit)
                if suit == firstSuit:
                    break

                continue

        waitingPatterns.append({"suit": suit.suit, "left": isLeftIrreducible, "right": isRightIrreducible, "isAcs": False, "suitNumber": suit.getSuitNumberWithACS(False)})
        # 雀頭接続順子のパターンの考慮
        if hand.hasAtamaConnectedShuntsuPattern():
            waitingPatterns.append({"suit": suit.suit, "left": isLeftIrreducible, "right": isRightIrreducible, "isAcs": True, "suitNumber": suit.getSuitNumberWithACS(True)})

        suit = SuitLoop.nextSuit(suit)
        if suit == firstSuit:
            break


def main(isSameWaiting):
    waitingPatterns = []
    getWaitingPatterns(waitingPatterns, 1, isSameWaiting)
    getWaitingPatterns(waitingPatterns, 2, isSameWaiting)
    getWaitingPatterns(waitingPatterns, 4, isSameWaiting)
    getWaitingPatterns(waitingPatterns, 5, isSameWaiting)
    getWaitingPatterns(waitingPatterns, 7, isSameWaiting)
    getWaitingPatterns(waitingPatterns, 8, isSameWaiting)
    getWaitingPatterns(waitingPatterns, 10, isSameWaiting)
    getWaitingPatterns(waitingPatterns, 11, isSameWaiting)
    getWaitingPatterns(waitingPatterns, 13, isSameWaiting)
    return setWaitingNumber(waitingPatterns)
