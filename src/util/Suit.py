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

    def __isFirstTIleZero(self) -> bool:
        return self.suit[0] == 0

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

    # ---------------------------------------------------------------------------- #
    # 牌くるくるに関する処理 ここから
    # ---------------------------------------------------------------------------- #

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

    def nextSuit(self) -> Self:
        """
        次の牌形を取得する
        """

        nextSuit = list(self.suit)

        while True:
            try:
                # 牌形の先頭が 0 かどうかで処理が分かれる
                return Suit(tuple(self.__nextSuitNonZeroFirst() if self.__isFirstTIleZero() else self.__nextSuitNonZeroFirst()))
            except ValueError:
                continue


    def __nextSuitNonZeroFirst(self) -> list[int]:
        """
        数牌の先頭が 0 でない時の処理

        Returns:
            list[int]: 次の数牌
        """

        suit = list(self.suit)
        suitLength: int = len(suit)
        index = 1

        # 先頭の数字を控えておく
        first = suit[0]
        # どの処理でも先頭は 0 になる
        suit[0] = 0

        while index < suitLength:
            # 0 でない数字を見つけた時
            if suit[index] != 0:
                # その場所の数字を 0 にする
                suit[index] -= 1
                # その前の場所の数字を先頭 + 1 の数字にする
                suit[index - 1] = first + 1
                return suit
            index += 1

        # 先頭以外で 0 が見つからなかった時は末尾を先頭の数字にする
        suit[suitLength - 1] = first
        return suit


    def __nextSuitZeroFirst(self) -> list[int]:
        """
        数牌の先頭が 0 である時の処理

        Returns:
            list[int]: 次の数牌
        """

        suit = list(self.suit)
        suitLength: int = len(suit)
        index: int = 0

        while index < suitLength:
            # 初めて 0 でない数字を見つけた時
            if suit[index] != 0:
                # その場所の数字を 1 引く
                suit[index] -= 1
                # その前の場所を 1 にする
                suit[index - 1] = 1
                return suit
            index += 1

        # ここに来ることはない
        raise RuntimeError("Unexpected error.")

    @staticmethod
    def getFirstSuit(number: int) -> Self:
        match number:
            case 1:
                return Suit((0, 0, 0, 0, 0, 0, 0, 0, 1))
            case 2:
                return Suit((0, 0, 0, 0, 0, 0, 0, 0, 2))
            case 4:
                return Suit((0, 0, 0, 0, 0, 0, 0, 0, 4))
            case 5:
                return Suit((0, 0, 0, 0, 0, 0, 0, 1, 4))
            case 7:
                return Suit((0, 0, 0, 0, 0, 0, 0, 3, 4))
            case 8:
                return Suit((0, 0, 0, 0, 0, 0, 0, 4, 4))
            case 10:
                return Suit((0, 0, 0, 0, 0, 0, 2, 4, 4))
            case 11:
                return Suit((0, 0, 0, 0, 0, 0, 3, 4, 4))
            case 13:
                return Suit((0, 0, 0, 0, 0, 1, 4, 4, 4))
            case _:
                raise ValueError("Wrong number.")

    # ---------------------------------------------------------------------------- #
    # 牌くるくるに関する処理 ここまで
    # ---------------------------------------------------------------------------- #
