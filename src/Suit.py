from dataclasses import dataclass
from typing import ClassVar, Optional

@dataclass(frozen=True)
class Suit:

    suit: list[int]
    MAX_TILE_COUNT: ClassVar[int] = 4
    SUIT_LENGTH: ClassVar[int] = 9

    def __init__(self, suit: list[int]):
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

    def isRegularForm(self) -> bool:
        return self.sum() % 3 == 1

    def isFirstTIleZero(self) -> bool:
        return self.suit[0] == 0

    def getRemainTileCount(self, index: int) -> int:
        if index < 0 or index >= self.SUIT_LENGTH:
            raise ValueError("Invalid index.")

        return self.MAX_TILE_COUNT - self.suit[index]

    # @todo 返り値の型を付ける
    def addTile(self, index: int):
        if index < 0 or index >= self.SUIT_LENGTH:
            raise ValueError("Invalid index.")

        resultSuit = self.suit.copy()
        resultSuit[index] += 1
        if resultSuit[index] > self.MAX_TILE_COUNT:
            return None

        return Suit(resultSuit)

    def getOneLeftSuit(self):
        resultSuit = []
        for index in range(1, self.length()):
            resultSuit.append(self.suit[index])

        resultSuit.append(0)
        return Suit(resultSuit)

    def getOneRightSuit(self):
        resultSuit = [0]
        for index in range(0, self.length() - 1):
            resultSuit.append(self.suit[index])

        return Suit(resultSuit)

    def getRightAttachSuit(self):
        resultSuit = self
        for _ in range(8 - self.getRange()):
            resultSuit = resultSuit.getOneRightSuit()

        return resultSuit

    def getReverseSuit(self):
        resultSuit = self.suit.copy()
        resultSuit.reverse()
        return Suit(resultSuit)

    def getRange(self) -> int:
        fisrtIndex = 0
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

    def isBasicForm(self) -> bool:
        """
        基本形かどうかを判定する

        判定方法:
            1. 後方重心なら基本形ではない
            2. 両接地なら基本形
            3. ゆとり 1 なら基本形
            4. 2 番目から始まっていたら基本形
            5. それ以外は基本形ではない

        Returns:
            bool: 基本形であれば True / そうでないとき False
        """

        suit = self.suit.copy()
        gravity: int = self.getSuitGravityPosition()

        # 後方重心なら基本形ではない
        if gravity == -1:
            return False

        # 両接地なら基本形
        if suit[0] != 0 and suit[-1] != 0:
            return True

        # ゆとりが 1 の時も基本形
        if (suit[0] == 0 and suit[1] != 0 and suit[-1] != 0) or (suit[0] != 0 and suit[-2] != 0 and suit[-1] == 0):
            return True

        # 2番目から始まっていた場合基本形
        if suit[0] == 0 and suit[1] != 0:
            return True

        # それ以外は基本形ではない
        return False


    def getSuitGravityPosition(self) -> int:
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
        suit = self.suit.copy()

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
