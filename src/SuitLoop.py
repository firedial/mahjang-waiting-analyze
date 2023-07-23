import src.Suit as Suit

"""
牌形を全パターン舐めるアルゴリズム(通称: 牌くるくる)

牌形を渡された時、先頭が 0 かどうかで処理を変える。
A: 先頭が 0 の時
    先頭から見ていき、初めて 0 でない数字を見つける。
    その場所の数字を 1 引いて、その前の場所の数字を 1 とする。
        例: [0, 0, 0, 3, 2]
            -> [0. 0. 1, 2, 2]
            -> [0. 1. 0, 2, 2]
            -> [1. 0. 0, 2, 2]
B: 先頭が 0 でない時
    先頭よりも後で 0 でない数字を見つける。
    見つけられなかった時は、末尾の数字を先頭の数字に、先頭の数字を 0 にして処理終了。
    見つけれれた場合、先頭の数字を控えておき 0 にする。
    見つかったその場所の数字を 1 引き、その前の場所の数字を先頭の数字 + 1 とする。
        例: [1, 0, 0, 2, 2]
            -> [0. 0. 2, 1, 2]

牌くるくるの動きの例
[0, 0, 4]
[0, 1, 3]
[1, 0, 3]
[0, 2, 2]
[1, 1, 2]
[2, 0, 2]
[0, 3, 1]
[1, 2, 1]
[2, 1, 1]
[3, 0, 1]
[0, 4, 0]
[1, 3, 0]
[2, 2, 0]
[3, 1, 0]
[4, 0, 0]
[0, 0, 4]
"""


def nextSuit(suit: Suit) -> Suit:
    """
    次の牌形を取得する

    Args:
        hand (Hand): 牌形

    Returns:
        Hand: 次の牌形
    """

    nextSuit = suit.suit.copy()

    while True:
        # 牌形の先頭が 0 かどうかで処理が分かれる
        nextHand = nextHandNonZeroFirst(nextSuit) if suit.isFirstTIleZero() else nextHandNonZeroFirst(nextSuit)
        try:
            return Suit.Suit(nextSuit)
        except:
            continue


def nextHandNonZeroFirst(hand: list[int]) -> list[int]:
    """
    牌形の先頭が 0 でない時の処理

    Args:
        hand (list[int]): 牌形

    Returns:
        list[int]: 次の牌形
    """

    handLength: int = len(hand)
    index = 1

    # 先頭の数字を控えておく
    first = hand[0]
    # どの処理でも先頭は 0 になる
    hand[0] = 0

    while index < handLength:
        # 0 でない数字を見つけた時
        if hand[index] != 0:
            # その場所の数字を 0 にする
            hand[index] -= 1
            # その前の場所の数字を先頭 + 1 の数字にする
            hand[index - 1] = first + 1
            return hand
        index += 1

    # 先頭以外で 0 が見つからなかった時は末尾を先頭の数字にする
    hand[handLength - 1] = first
    return hand

def nextHandZeroFirst(hand: list[int]) -> list[int]:
    """
    牌形の先頭が 0 である時の処理

    Args:
        hand (list[int]): 牌形

    Returns:
        list[int]: 次の牌形
    """

    handLength: int = len(hand)
    index: int = 0

    while index < handLength:
        # 初めて 0 でない数字を見つけた時
        if hand[index] != 0:
            # その場所の数字を 1 引く
            hand[index] -= 1
            # その前の場所を 1 にする
            hand[index - 1] = 1
            return hand
        index += 1


    # ここに来ることはない
    raise RuntimeError("Unexpected error.")

