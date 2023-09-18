from dataclasses import dataclass
from typing import ClassVar
from src.util.Block import Block
from functools import cached_property
from src.util.WaitingType import WaitingType
from src.util.WaitingStructure import WaitingStructure
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

    def sum(self) -> int:
        return sum(self.suit)

    # ---------------------------------------------------------------------------- #
    # 牌除去に関する処理 ここから
    # ---------------------------------------------------------------------------- #

    def __getRemovedBlockPatterns(self, block: Block) -> list[Self]:
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


    def __getRemovedMultiBlockPatterns(self, blocks: list[Block]) -> list[Self]:
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
            removedSuits += self.__getRemovedBlockPatterns(block)

        return removedSuits


    def getRemovedAtamaPatterns(self) -> list[Self]:
        """
        雀頭のパターンを省けるだけ省いた数牌のリストを返す

        Returns:
            lits[Self]: 数牌から面子のパターンを省いた牌形のリスト
        """
        return self.__getRemovedBlockPatterns(Block((2, )))


    def getRemovedAtamaConnectedShuntsuPatterns(self) -> list[Self]:
        """
        雀頭接続順子のパターンを省けるだけ省いた数牌のリストを返す

        Returns:
            lits[Self]: 牌形から雀頭接続順子のパターンを省いた数牌のリスト
        """
        return self.__getRemovedMultiBlockPatterns([Block((3, 1, 1, 0)), Block((0, 1, 1, 3))])


    def getRemovedMentsuPatterns(self) -> list[Self]:
        """
        面子(刻子と順子)のパターンを省けるだけ省いた数牌のリストを返す

        Returns:
            lits[Self]: 牌形から面子のパターンを省いた数牌のリスト
        """
        return self.__getRemovedMultiBlockPatterns([Block((3, )), Block((1, 1, 1))])

    # ---------------------------------------------------------------------------- #
    # 牌除去に関する処理 ここまで
    # ---------------------------------------------------------------------------- #

    # ---------------------------------------------------------------------------- #
    # 和了に関する処理 ここから
    # ---------------------------------------------------------------------------- #

    def __getTankiJudgeSuit(self, index: int) -> Self:
        if index < 0 or index >= self.SUIT_LENGTH:
            return None

        if self.suit[index] == 0:
            return None

        return Suit(self.suit[:index] + (self.suit[index] - 1, ) + self.suit[index + 1:])

    def __getShamponJudgeSuit(self, index: int) -> Self:
        if index < 0 or index >= self.SUIT_LENGTH:
            return None

        if self.suit[index] < 2:
            return None

        return Suit(self.suit[:index] + (self.suit[index] - 2, ) + self.suit[index + 1:])

    def __getKanchanJudgeSuit(self, index: int) -> Self:
        if index < 1 or index >= self.SUIT_LENGTH - 1:
            return None

        if self.suit[index - 1] == 0 or self.suit[index + 1] == 0:
            return None

        return Suit(self.suit[:index - 1] + (self.suit[index - 1] - 1, self.suit[index], self.suit[index + 1] - 1) + self.suit[index + 2:])

    def __getRyanmenLeftJudgeSuit(self, index: int) -> Self:
        if index < 0 or index >= self.SUIT_LENGTH - 2:
            return None

        if self.suit[index + 1] == 0 or self.suit[index + 2] == 0:
            return None

        return Suit(self.suit[:index] + (self.suit[index], self.suit[index + 1] - 1, self.suit[index + 2] - 1) + self.suit[index + 3:])

    def __getRyanmenRightJudgeSuit(self, index: int) -> Self:
        if index < 2 or index >= self.SUIT_LENGTH:
            return None

        if self.suit[index - 1] == 0 or self.suit[index - 2] == 0:
            return None

        return Suit(self.suit[:index - 2] + (self.suit[index - 2] - 1, self.suit[index - 1] - 1, self.suit[index]) + self.suit[index + 1:])

    def __isAgari(self) -> bool:
        """
        渡された数牌が和了形であるかどうかを判定する

        牌の枚数によって判定条件が変わる
            3n + 2 枚のとき: 1 雀頭 n 面子のときに限り和了形
            3n + 1 枚のとき: 和了形にならない
            3n 枚のとき: n 面子のときに限り和了形

        Returns:
            bool: 和了形であれば True / そうでないとき False

        """
        # 手牌の牌の合計枚数
        suitTileCount: int = self.sum()

        # 手牌の合計枚数が0なら和了形
        if suitTileCount == 0:
            return True

        # 枚数が 3n + 1 場合は和了形にならない
        if suitTileCount % 3 == 1:
            return False

        # 枚数が 3n + 2 場合は頭を除去する
        if suitTileCount % 3 == 2:
            for h in self.getRemovedAtamaPatterns():
                if h.__isAgari():
                    return True
            else:
                return False

        # 3n 枚の時のは面子の除去
        for h in self.getRemovedMentsuPatterns():
            if h.__isAgari():
                return True
        else:
            return False

    @cached_property
    def waitingStructure(self) -> WaitingStructure:
        waitingStructures = []
        for index in range(self.length()):
            tankiJudgeSuit = self.__getTankiJudgeSuit(index)
            shamponJudgeSuit = self.__getShamponJudgeSuit(index)
            kanchanJudgeSuit = self.__getKanchanJudgeSuit(index)
            ryanmenLeftJudgeSuit = self.__getRyanmenLeftJudgeSuit(index)
            ryanmenRightJudgeSuit = self.__getRyanmenRightJudgeSuit(index)

            waitingStructures.append(
                WaitingType(
                    isTanki = False if tankiJudgeSuit is None else tankiJudgeSuit.__isAgari(),
                    isShampon = False if shamponJudgeSuit is None else shamponJudgeSuit.__isAgari(),
                    isKanchan = False if kanchanJudgeSuit is None else kanchanJudgeSuit.__isAgari(),
                    isRyanmenLeft = False if ryanmenLeftJudgeSuit is None else ryanmenLeftJudgeSuit.__isAgari(),
                    isRyanmenRight = False if ryanmenRightJudgeSuit is None else ryanmenRightJudgeSuit.__isAgari(),
                )
            )

        return WaitingStructure(tuple(waitingStructures))

    # ---------------------------------------------------------------------------- #
    # 和了に関する処理 ここまで
    # ---------------------------------------------------------------------------- #

