from dataclasses import dataclass
from typing import ClassVar, Self
from src.util.Block import Block
from functools import cached_property
from src.util.WaitingType import WaitingType
from src.util.WaitingStructure import WaitingStructure


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
            if waitingType.hasWaiting():
                return True
        else:
            return False

    def isTempaiWithoutTileCount(self) -> bool:
        for waitingType in self.waitingStructure.waitingStructures:
            if waitingType.hasWaiting():
                return True
        else:
            return False

    def isSendable(self) -> bool:
        return self.__isAgari()

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

    def getSuitNumber(self) -> int:
        leftAttachedSuit = self.getLeftAttachSuit()

        countMap = {1: 9, 2: 8, 4: 7, 5: 6, 7: 5, 8: 4, 10: 3, 11: 2, 13: 1}
        handCount = self.sum() + (2 if not self.__isRegularForm() else 0)
        number = countMap[handCount] * 10 + countMap[self.sum()]
        for tile in leftAttachedSuit.suit:
            number = number * 10 + tile

        return number

    def __isRegularForm(self) -> bool:
        return self.sum() % 3 == 1

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

    def __getSuitString(self) -> str:
        return ''.join(map(lambda x: str(x), self.suit))

    # ---------------------------------------------------------------------------- #
    # 基本形に関する処理 ここから
    # ---------------------------------------------------------------------------- #

    def isWaitingTileBasicForm(self) -> bool:
        """
        待ち牌基本形かどうかを判定する

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

    def isWaitingStructureBasicForm(self) -> bool:
        """
        待ち構造基本形かどうかを判定する

        判定方法:
            1. 後方重心なら基本形ではない
            2. 両接地なら基本形
            3. 1 番目から始まっていたら基本形
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

        # 1番目から始まっていた場合基本形
        if suit[0] != 0:
            return True

        # それ以外は基本形ではない
        return False

    def __getWaitingStructureBasicForm(self) -> Self:
        suit = self

        # 後方重心なら前方重心にする
        if suit.__getSuitGravityPosition() < 0:
            suit = Suit(suit.suit[::-1])

        # 左接地するものを返す
        return suit.getLeftAttachSuit()

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

    def __getRemovedAtamaPatterns(self) -> list[Self]:
        """
        雀頭のパターンを省けるだけ省いた数牌のリストを返す

        Returns:
            lits[Self]: 数牌から面子のパターンを省いた牌形のリスト
        """
        return self.__getRemovedBlockPatterns(Block((2, )))

    def __getRemovedAtamaConnectedShuntsuPatterns(self) -> list[Self]:
        """
        雀頭接続順子のパターンを省けるだけ省いた数牌のリストを返す

        Returns:
            lits[Self]: 牌形から雀頭接続順子のパターンを省いた数牌のリスト
        """
        return self.__getRemovedMultiBlockPatterns([Block((3, 1, 1)), Block((1, 1, 3))])

    def __getRemovedMentsuPatterns(self) -> list[Self]:
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
        if index < 2 or index >= self.SUIT_LENGTH:
            return None

        if self.suit[index - 1] == 0 or self.suit[index - 2] == 0:
            return None

        return Suit(self.suit[:index - 2] + (self.suit[index - 2] - 1, self.suit[index - 1] - 1, self.suit[index]) + self.suit[index + 1:])

    def __getRyanmenRightJudgeSuit(self, index: int) -> Self:
        if index < 0 or index >= self.SUIT_LENGTH - 2:
            return None

        if self.suit[index + 1] == 0 or self.suit[index + 2] == 0:
            return None

        return Suit(self.suit[:index] + (self.suit[index], self.suit[index + 1] - 1, self.suit[index + 2] - 1) + self.suit[index + 3:])

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
            for h in self.__getRemovedAtamaPatterns():
                if h.__isAgari():
                    return True
            else:
                return False

        # 3n 枚の時のは面子の除去
        for h in self.__getRemovedMentsuPatterns():
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

    def isWaitingStructureIrreducible(self) -> bool:
        # 面子の既約
        if not self.__isFormWaitingStructureIrreducible(self.__getRemovedMentsuPatterns()):
            return False

        # 正規形のときは待ち送り形の既約もみる
        if self.__isRegularForm():
            if not self.__isFormWaitingStructureIrreducible(self.__getRemovedAtamaPatterns()) or not self.__isFormWaitingStructureIrreducible(self.__getRemovedAtamaConnectedShuntsuPatterns()):
                return False

        return True

    def __isFormWaitingStructureIrreducible(self, suits: list[Self]) -> bool:
        for suit in suits:
            if self.__isSameWaitingStructure(suit):
                return False
        else:
            return True

    def __isSameWaitingStructure(self, removedSuit: Self) -> bool:
        def isSame(a: WaitingStructure, b: WaitingStructure):
            return a == b

        index, removePattern = self.__getRemovePattern(removedSuit)

        # 面子除去のとき
        if removePattern == 0:
            return isSame(self.waitingStructure, removedSuit.waitingStructure) and self.isSendable() == removedSuit.isSendable()

        # 雀頭除去のとき
        if removePattern == 2:
            # 待ち送り系でシャンポン待ちであるとき
            if removedSuit.isSendable() and self.waitingStructure.waitingStructures[index].isShampon:
                return isSame(self.waitingStructure, removedSuit.waitingStructure.addAtama(index))
            else:
                return isSame(self.waitingStructure, removedSuit.waitingStructure)

        # 雀頭接続順子(113)除去のとき
        if removePattern == 113 or removePattern == 311:
            # 待ち送り系でシャンポン待ちであるとき
            if removedSuit.isSendable() and self.waitingStructure.waitingStructures[index].isShampon:
                return isSame(self.waitingStructure, removedSuit.waitingStructure.addAtamaConnectedShuntsu(index, removePattern))
            else:
                return isSame(self.waitingStructure, removedSuit.waitingStructure)

        raise ValueError("Unexpected pattern.")

    def isWaitingTileIrreducible(self) -> bool:
        # 面子の既約
        if not self.__isFormWaitingTileIrreducible(self.__getRemovedMentsuPatterns()):
            return False

        # 正規形のときは待ち送り形の既約もみる
        if self.__isRegularForm():
            if not self.__isFormWaitingTileIrreducible(self.__getRemovedAtamaPatterns()) or not self.__isFormWaitingTileIrreducible(self.__getRemovedAtamaConnectedShuntsuPatterns()):
                return False

        return True

    def __isFormWaitingTileIrreducible(self, suits: list[Self]) -> bool:
        for suit in suits:
            if self.__isSameWaitingTile(suit):
                return False
        else:
            return True

    def __isSameWaitingTile(self, removedSuit: Self) -> bool:
        def isSame(a: WaitingStructure, b: WaitingStructure):
            for x, y in zip(a.waitingStructures, b.waitingStructures):
                if x.hasWaiting() != y.hasWaiting():
                    return False
            else:
                return True

        index, removePattern = self.__getRemovePattern(removedSuit)

        # 面子除去のとき
        if removePattern == 0:
            return isSame(self.waitingStructure, removedSuit.waitingStructure) and self.isSendable() == removedSuit.isSendable()

        # 雀頭除去のとき
        if removePattern == 2:
            # 待ち送り系でシャンポン待ちであるとき
            if removedSuit.isSendable() and self.waitingStructure.waitingStructures[index].isShampon:
                return isSame(self.waitingStructure, removedSuit.waitingStructure.addAtama(index))
            else:
                return isSame(self.waitingStructure, removedSuit.waitingStructure)

        # 雀頭接続順子(113)除去のとき
        if removePattern == 113 or removePattern == 311:
            # 待ち送り系でシャンポン待ちであるとき
            if removedSuit.isSendable() and self.waitingStructure.waitingStructures[index].isShampon:
                return isSame(self.waitingStructure, removedSuit.waitingStructure.addAtamaConnectedShuntsu(index, removePattern))
            else:
                return isSame(self.waitingStructure, removedSuit.waitingStructure)

        raise ValueError("Unexpected pattern.")

    def __getRemovePattern(self, removedSuit: Self) -> tuple[int, int]:
        # 除去した牌が面子の場合
        if self.sum() - removedSuit.sum() == 3:
            return (0, 0)

        hasOne = False
        for index in range(self.SUIT_LENGTH):
            diff = self.suit[index] - removedSuit.suit[index]
            if diff == 0:
                continue

            # 除去した牌が雀頭の場合
            if diff == 2:
                return (index, 2)

            # 既に1があったかどうか
            if diff == 1:
                hasOne = True
                continue

            # 除去した牌が雀頭接続順子の場合
            if diff == 3:
                return (index, 113) if hasOne else (index, 311)

        raise ValueError("Unexpected pattern.")

    # ---------------------------------------------------------------------------- #
    # 既約に関する処理 ここまで
    # ---------------------------------------------------------------------------- #

    # ---------------------------------------------------------------------------- #
    # 構造一意に関する処理 ここから
    # ---------------------------------------------------------------------------- #

    # @todo self 使っていない
    def getWaitingStructurePossiblePattern(self, suit, waitingStructurePatterns: dict, waitingStructurePossiblePatterns: list):
        # 構造既約かどうかの確認
        number = waitingStructurePatterns.get(suit.__getWaitingStructureBasicForm().__getSuitString())
        if number is not None:
            return waitingStructurePossiblePatterns.append(number)

        # 面子の除去
        for removed in suit.__getRemovedMentsuPatterns():
            # 既約じゃなくなっていたら考慮しない
            if not suit.__isSameWaitingStructure(removed):
                continue

            removed.getWaitingStructurePossiblePattern(removed, waitingStructurePatterns, waitingStructurePossiblePatterns)

        # 正規形のときは待ち送り形の除去
        if suit.__isRegularForm():
            for removed in suit.__getRemovedAtamaPatterns() + suit.__getRemovedAtamaConnectedShuntsuPatterns():
                # 既約じゃなくなっていたら考慮しない
                if not suit.__isSameWaitingStructure(removed):
                    continue

                removed.getWaitingStructurePossiblePattern(removed, waitingStructurePatterns, waitingStructurePossiblePatterns)

    # ---------------------------------------------------------------------------- #
    # 構造一意に関する処理 ここまで
    # ---------------------------------------------------------------------------- #
