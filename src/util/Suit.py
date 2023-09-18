from dataclasses import dataclass
from typing import ClassVar
from src.util.Block import Block
from typing import Self


@dataclass(frozen=True)
class Suit:

    suit: tuple[int, ...]
    MAX_TILE_COUNT: ClassVar[int] = 4
    SUIT_LENGTH: ClassVar[int] = 9

    def __init__(self, suit: tuple[int, ...]):
        if len(suit) != self.SUIT_LENGTH:
            raise ValueError("Wrong suit length.")

        for tile in suit:
            if tile > self.MAX_TILE_COUNT or tile < 0:
                raise ValueError("Wrong tile count.")

        object.__setattr__(self, "suit", suit)

    def length(self) -> int:
        return len(self.suit)

    # ---------------------------------------------------------------------------- #
    # 牌除去に関する処理 ここから
    # ---------------------------------------------------------------------------- #

    def getRemovedBlockPatterns(self, block: Block) -> list[Self]:
        """
        数牌から牌を除去できるパターンのリストを返す

        Args:
            block (Block): 除去する牌

        Returns:
            list[Self]: 除去できるパターンのリスト
        """
        # 除去処理のループを回す回数を求める
        loopCount: int = self.length() - block.length() + 1

        # 除去した数牌を格納する
        removedSuits: list[Self] = []

        for x in range(0, loopCount):
            tmpSuit = list(self.suit)
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


    def getRemovedMultiBlockPatterns(self, blocks: list[Block]) -> list[Self]:
        """
        数牌から牌を除去できるパターンのリストを返す

        Args:
            blocks (list[Block]): 除去する牌のリスト

        Returns:
            list[Self]: 除去できるパターンのリスト
        """
        # 除去した数牌を格納する
        removedSuits: list[Self] = []

        for block in blocks:
            removedSuits += self.getRemovedBlockPatterns(block)

        return removedSuits


    def getRemovedAtamaPatterns(self) -> list[Self]:
        """
        雀頭のパターンを省けるだけ省いた数牌のリストを返す

        Returns:
            lits[Self]: 数牌から面子のパターンを省いた牌形のリスト
        """
        return self.getRemovedBlockPatterns(Block((2, )))


    def getRemovedAtamaConnectedShuntsuPatterns(self) -> list[Self]:
        """
        雀頭接続順子のパターンを省けるだけ省いた数牌のリストを返す

        Returns:
            lits[Self]: 牌形から雀頭接続順子のパターンを省いた数牌のリスト
        """
        return self.getRemovedMultiBlockPatterns([Block((3, 1, 1, 0)), Block((0, 1, 1, 3))])


    def getRemovedMentsuPatterns(self) -> list[Self]:
        """
        面子(刻子と順子)のパターンを省けるだけ省いた数牌のリストを返す

        Returns:
            lits[Self]: 牌形から面子のパターンを省いた数牌のリスト
        """
        return self.getRemovedMultiBlockPatterns([Block((3, )), Block((1, 1, 1))])

    # ---------------------------------------------------------------------------- #
    # 牌除去に関する処理 ここまで
    # ---------------------------------------------------------------------------- #

