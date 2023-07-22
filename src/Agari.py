from src.Hand import Hand
import src.Remove as Remove
import src.Waiting as Waiting

def isAgari(hand: Hand) -> bool:
    """
    渡された牌形が和了形であるかどうかを判定する

    牌の枚数によって判定条件が変わる
        3n + 2 枚のとき: 1 雀頭 n 面子のときに限り和了形
        3n + 1 枚のとき: 和了形にならない
        3n 枚のとき: n 面子のときに限り和了形

    Args:
        hand (Hand): 牌形

    Returns:
        bool: 和了形であれば True / そうでないとき False

    """
    # 手牌の牌の合計枚数
    handTileCount: int = hand.sum()

    # 手牌の合計枚数が0なら和了形
    if handTileCount == 0:
        return True

    # 枚数が 3n + 1 場合は和了形にならない
    if handTileCount % 3 == 1:
        return False

    # 枚数が 3n + 2 場合は頭を除去する
    if handTileCount % 3 == 2:
        for h in Remove.getRemovedAtamaPatterns(hand):
            if isAgari(h):
                return True
        else:
            return False

    # 3n 枚の時のは面子の除去
    for h in Remove.getRemovedMentsuPatterns(hand):
        if isAgari(h):
            return True
    else:
        return False


def getWaiting(hand: Hand) -> Waiting:
    waitingCount = []

    for index in range(hand.length()):
        # 一枚牌を追加する
        addedTileHand = hand.addTile(index)

        # 追加できなかったときは次のループへ
        if addedTileHand is None:
            waitingCount.append(0)
            continue

        if isAgari(addedTileHand):
            waitingCount.append(hand.getRemainTileCount(index))
        else:
            waitingCount.append(0)

    # 待ち送り系かどうか
    isSendable = isAgari(hand)

    return Waiting.Waiting(waitingCount, isSendable)
