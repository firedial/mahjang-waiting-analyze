from src.util.Suit import Suit
import src.util.SuitLoop as SuitLoop


def sortWaitingTilePattern(waitingPatterns: list) -> list:
    sortedPatterns = sorted(waitingPatterns, key = lambda x: x['suitNumber'], reverse = True)
    count = 0
    for pattern in sortedPatterns:
        count += 1
        pattern.pop("suitNumber")

    return sortedPatterns


def getWaitingPatterns(suit: Suit):
    # 基本形ではない時は考慮外
    if not suit.isWaitingTileBasicForm():
        return None

    # 両接地形
    if suit.isRangeFull():
        # 聴牌形、既約系でなければ考慮外
        if not (suit.isTempai() and suit.isWaitingTileIrreducible()):
            return None

        isRightIrreducible = True
        isLeftIrreducible = True

    # 片接地形
    elif suit.hasOneRoomRange():
        # 右接地パターン
        rightAttachSuit = suit
        isRightIrreducible = rightAttachSuit.isTempai() and rightAttachSuit.isWaitingTileIrreducible()

        # 左接地パターン
        leftAttachSuit = suit.getLeftAttachSuit()
        isLeftIrreducible = leftAttachSuit.isTempai() and leftAttachSuit.isWaitingTileIrreducible()

        # どっちに接地していても既約でない場合は登録しない
        if (not isRightIrreducible) and (not isLeftIrreducible):
            return None

    else:
        # 範囲が7以下のときは、移動系と右接地と左接地について見る

        # 無接地パターン
        isCenterIrreducible = suit.isTempai() and suit.isWaitingTileIrreducible()

        # 右接地パターン
        rightAttachSuit = suit.getRightAttachSuit()
        isRightIrreducible = rightAttachSuit.isTempai() and rightAttachSuit.isWaitingTileIrreducible()

        # 左接地パターン
        leftAttachSuit = suit.getLeftAttachSuit()
        isLeftIrreducible = leftAttachSuit.isTempai() and leftAttachSuit.isWaitingTileIrreducible()

        # 無接地は既約じゃないが、接地パターンが既約になる場合はない想定
        if not isCenterIrreducible and (isRightIrreducible or isLeftIrreducible):
            raise RuntimeError("Unexpected error.")

        # 既約でない場合は登録しない
        if not isCenterIrreducible:
            return None

    return {"suit": suit.suit, "left": isLeftIrreducible, "right": isRightIrreducible, "suitNumber": suit.getSuitNumber()}


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
    return sortWaitingTilePattern(waitingPatterns)
