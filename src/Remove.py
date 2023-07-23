from src.Suit import Suit
from src.Block import Block

def getRemovedBlockPatterns(hand: Suit, block: Block) -> list[Suit]:
    """
    手牌から牌を除去できるパターンのリストを返す

    Args:
        hand (Hand): 牌形
        block (Block): 除去する牌

    Returns:
        list[Hand]: 除去できるパターンのリスト
    """
    # 除去処理のループを回す回数を求める
    loopCount: int = hand.length() - block.length() + 1

    # 除去した牌形を格納する
    removedHands: list[Hand] = []

    for x in range(0, loopCount):
        tmpHand = hand.hand[:]
        for index, count in enumerate(block.block):
            # 牌形から牌を除去する
            tmpHand[x + index] -= count
            # 途中で 0 未満になったら抜ける
            if tmpHand[x + index] < 0:
                break
        else:
            # 全て 0 以上なのでリストに追加する
            removedHands.append(Suit(tmpHand))

    return removedHands

def getRemovedMultiBlockPatterns(hand: Suit, blocks: list[Block]) -> list[Suit]:
    """
    手牌から牌を除去できるパターンのリストを返す

    Args:
        hand (Hand): 牌形
        blocks (list[Block]): 除去する牌のリスト

    Returns:
        list[Hand]: 除去できるパターンのリスト
    """
    # 除去した牌形を格納する
    removedHands: list[Hand] = []

    for block in blocks:
        removedHands += getRemovedBlockPatterns(hand, block)

    return removedHands

def getRemovedAtamaPatterns(hand: Suit) -> list[Suit]:
    """
    雀頭のパターンを省けるだけ省いた牌形のリストを返す

    Args:
        hand (Hand): 牌形

    Returns:
        lits[Hand]: 牌形から面子のパターンを省いた牌形のリスト
    """
    return getRemovedBlockPatterns(hand, Block([2]))

def getRemovedKotsuPatterns(hand: Suit) -> list[Suit]:
    """
    刻子のパターンを省けるだけ省いた牌形のリストを返す

    Args:
        hand (Hand): 牌形

    Returns:
        lits[Hand]: 牌形から刻子のパターンを省いた牌形のリスト
    """
    return getRemovedBlockPatterns(hand, Block([3]))

def getRemovedShuntsuPatterns(hand: Suit) -> list[Suit]:
    """
    順子のパターンを省けるだけ省いた牌形のリストを返す

    Args:
        hand (Hand): 牌形

    Returns:
        lits[Hand]: 牌形から順子のパターンを省いた牌形のリスト
    """
    return getRemovedBlockPatterns(hand, Block([1, 1, 1]))

def getRemovedAtamaConnectedShuntsuPatterns(hand: Suit) -> list[Suit]:
    """
    雀頭接続順子のパターンを省けるだけ省いた牌形のリストを返す

    Args:
        hand (Hand): 牌形

    Returns:
        lits[Hand]: 牌形から雀頭接続順子のパターンを省いた牌形のリスト
    """
    return getRemovedMultiBlockPatterns(hand, [Block([3, 1, 1, 0]), Block([0, 1, 1, 3])])

def getRemovedMentsuPatterns(hand: Suit) -> list[Suit]:
    """
    面子(刻子と順子)のパターンを省けるだけ省いた牌形のリストを返す

    Args:
        hand (Hand): 牌形

    Returns:
        lits[Hand]: 牌形から面子のパターンを省いた牌形のリスト
    """
    return getRemovedKotsuPatterns(hand) + getRemovedShuntsuPatterns(hand)

def getRemovedSendableFormPatterns(hand: Suit) -> list[Suit]:
    """
    待ち送り系のパターンを省けるだけ省いた牌形のリストを返す

    Args:
        hand (Hand): 牌形

    Returns:
        lits[Hand]: 牌形から待ち送り系のパターンを省いた牌形のリスト
    """
    return getRemovedAtamaPatterns(hand) + getRemovedAtamaConnectedShuntsuPatterns(hand)
