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

    def isTempai(self) -> bool:
        for tile, waitingType in zip(self.suit, self.waitingStructure.waitingStructures):
            if tile < self.MAX_TILE_COUNT and waitingType.hasWaiting():
                return True
        else:
            return False

    def isRangeFull(self) -> bool:
        return self.__getRange() == self.SUIT_LENGTH

    def hasOneRoomRange(self) -> bool:
        return self.__getRange() == self.SUIT_LENGTH - 1

    def getLeftAttachSuit(self) -> Self:
        suit = self
        for _ in range(self.__getPosition()):
            suit = suit.__getOneLeftSuit()

        return suit

    def getRightAttachSuit(self) -> Self:
        suit = self
        for _ in range(self.SUIT_LENGTH - self.__getPosition() - self.__getRange()):
            suit = suit.__getOneRightSuit()

        return suit

    def __getOneLeftSuit(self) -> Self:
        resultSuit = []
        for index in range(1, self.length()):
            resultSuit.append(self.suit[index])

        resultSuit.append(0)
        return Suit(tuple(resultSuit))

    def __getOneRightSuit(self) -> Self:
        resultSuit = [0]
        for index in range(0, self.length() - 1):
            resultSuit.append(self.suit[index])

        return Suit(tuple(resultSuit))

    def __getPosition(self) -> int:
        for index in range(self.length()):
            if self.suit[index] != 0:
                return index

        raise ValueError("Suit is all zero.")

    def __getRange(self) -> int:
        firstIndex = 0
        for index in range(self.length()):
            if self.suit[index] != 0:
                firstIndex = index
                break

        lastIndex = self.length() - 1
        for index in range(self.length()):
            if self.suit[self.length() - 1 - index] != 0:
                lastIndex = self.length() - 1 - index
                break

        return lastIndex - firstIndex + 1

    def isFirstTIleZero(self) -> bool:
        return self.suit[0] == 0

    # ---------------------------------------------------------------------------- #
    # 標準形に関する処理 ここから
    # ---------------------------------------------------------------------------- #

    def isBasicForm(self) -> bool:
        """
        基本形かどうかを判定する

        判定方法:
            1. 後方重心なら基本形ではない
            2. 両接地なら基本形
            3. 2 番目から始まっていたら基本形
            4. それ以外は基本形ではない

        Returns:
            bool: 基本形であれば True / そうでないとき False
        """

        suit = list(self.suit)
        gravity: int = self.__getSuitGravityPosition()

        # 後方重心なら基本形ではない
        if gravity == -1:
            return False

        # 両接地なら基本形
        if suit[0] != 0 and suit[-1] != 0:
            return True

        # 2番目から始まっていた場合基本形
        if suit[0] == 0 and suit[1] != 0:
            return True

        # それ以外は基本形ではない
        return False

    def __getSuitGravityPosition(self) -> int:
        """
        数牌の重心を求める

        両端に接地している連続する 0 を無視する。
        両端から見て行った時、大きい数字がある方に重心がある。
        同じ場合はさらに一つ内側で比較する。最後まで一緒なら左右対称形。

        例:
            [0, 2, 4, 0, 0] -> 後方重心
            [0, 2, 2, 3, 2] -> 後方重心
            [0, 2, 2, 1, 2] -> 前方重心
            [0, 2, 1, 1, 2, 0, 0] -> 左右対称形

        Returns:
            int: 前方重心 1 / 左右対称 0 / 後方重心 -1

        """
        suitLength: int = self.length()
        suit = list(self.suit)

        first: int = 0
        last: int = suitLength - 1

        # 前から見たときに初めて 0 でない場所を見つける
        while first < suitLength:
            if suit[first] != 0:
                break
            first += 1

        # 後ろから見たときに初めて 0 でない場所を見つける
        while 0 <= last:
            if suit[last] != 0:
                break
            last -= 1

        # 両端から重心を見ていく
        while first < last:
            if suit[first] > suit[last]:
                # 前方重心
                return 1
            if suit[first] < suit[last]:
                # 後方重心
                return -1
            first += 1
            last -= 1

        # 左右対称形
        return 0

    # ---------------------------------------------------------------------------- #
    # 標準形に関する処理 ここまで
    # ---------------------------------------------------------------------------- #

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
    # 既約に関する処理 ここから
    # ---------------------------------------------------------------------------- #

    def isIrreducible(self) -> bool:
        # @todo 後で実装する
        return True

    # ---------------------------------------------------------------------------- #
    # 既約に関する処理 ここまで
    # ---------------------------------------------------------------------------- #
