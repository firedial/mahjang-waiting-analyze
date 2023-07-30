from src.Suit import Suit
from src.Block import Block

def getRemovedBlockPatterns(suit: Suit, block: Block) -> list[Suit]:
    """
    数牌から牌を除去できるパターンのリストを返す

    Args:
        suit (Suit): 数牌
        block (Block): 除去する牌

    Returns:
        list[Suit]: 除去できるパターンのリスト
    """
    # 除去処理のループを回す回数を求める
    loopCount: int = suit.length() - block.length() + 1

    # 除去した数牌を格納する
    removedSuits: list[Suit] = []

    for x in range(0, loopCount):
        tmpSuit = list(suit.suit)
        for index, count in enumerate(block.block):
            # 数牌から牌を除去する
            tmpSuit[x + index] -= count
            # 途中で 0 未満になったら抜ける
            if tmpSuit[x + index] < 0:
                break
        else:
            # 全て 0 以上なのでリストに追加する
            removedSuits.append(Suit(tuple(tmpSuit)))

    return removedSuits

def getRemovedMultiBlockPatterns(suit: Suit, blocks: list[Block]) -> list[Suit]:
    """
    数牌から牌を除去できるパターンのリストを返す

    Args:
        suit (Suit): 数牌
        blocks (list[Block]): 除去する牌のリスト

    Returns:
        list[Suit]: 除去できるパターンのリスト
    """
    # 除去した数牌を格納する
    removedSuits: list[Suit] = []

    for block in blocks:
        removedSuits += getRemovedBlockPatterns(suit, block)

    return removedSuits

def getRemovedAtamaPatterns(suit: Suit) -> list[Suit]:
    """
    雀頭のパターンを省けるだけ省いた数牌のリストを返す

    Args:
        suit (Suit): 数牌

    Returns:
        lits[Suit]: 数牌から面子のパターンを省いた牌形のリスト
    """
    return getRemovedBlockPatterns(suit, Block((2, )))

def getRemovedAtamaConnectedShuntsuPatterns(suit: Suit) -> list[Suit]:
    """
    雀頭接続順子のパターンを省けるだけ省いた数牌のリストを返す

    Args:
        suit (Suit): 牌形

    Returns:
        lits[Suit]: 牌形から雀頭接続順子のパターンを省いた数牌のリスト
    """
    return getRemovedMultiBlockPatterns(suit, [Block((3, 1, 1, 0)), Block((0, 1, 1, 3))])

def getRemovedMentsuPatterns(suit: Suit) -> list[Suit]:
    """
    面子(刻子と順子)のパターンを省けるだけ省いた数牌のリストを返す

    Args:
        suit (Suit): 牌形

    Returns:
        lits[Suit]: 牌形から面子のパターンを省いた数牌のリスト
    """
    return getRemovedMultiBlockPatterns(suit, [Block((3, )), Block((1, 1, 1))])
