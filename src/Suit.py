from dataclasses import dataclass
from typing import ClassVar, Optional

@dataclass(frozen=True)
class Suit:

    hand: list[int]
    suit: list[int]
    MAX_TILE_COUNT: ClassVar[int] = 4
    HAND_LENGTH: ClassVar[int] = 9

    def __init__(self, hand: list[int]):
        if len(hand) != self.HAND_LENGTH:
            raise ValueError("Wrong hand length.")

        for tile in hand:
            if tile > self.MAX_TILE_COUNT or tile < 0:
                raise ValueError("Wrong tile count.")

        object.__setattr__(self, "hand", hand)
        object.__setattr__(self, "suit", hand)

    def length(self) -> int:
        return len(self.hand)

    def sum(self) -> int:
        return sum(self.hand)

    def isRegularForm(self) -> bool:
        return self.sum() % 3 == 1

    def isFirstTIleZero(self) -> bool:
        return self.hand [0] == 0

    def getRemainTileCount(self, index: int) -> int:
        if index < 0 or index >= self.HAND_LENGTH:
            raise ValueError("Invalid index.")

        return self.MAX_TILE_COUNT - self.hand[index]

    # @todo 返り値の型を付ける
    def addTile(self, index: int):
        if index < 0 or index >= self.HAND_LENGTH:
            raise ValueError("Invalid index.")

        resultHand = self.hand.copy()
        resultHand[index] += 1
        if resultHand[index] > self.MAX_TILE_COUNT:
            return None

        return Suit(resultHand)


    def isBasicForm(self) -> bool:
        """
        基本形かどうかを判定する

        判定方法:
            1. 後方重心なら基本形ではない
            2. 両接地なら基本形
            3. ゆとり 1 なら基本形
            4. 2 番目から始まっていたら基本形
            5. それ以外は基本形ではない

        Args:
            hand (lsit[int]): 牌形

        Returns:
            bool: 基本形であれば True / そうでないとき False
        """

        hand = self.hand.copy()
        gravity: int = self.getHandGravityPosition()

        # 後方重心なら基本形ではない
        if gravity == -1:
            return False

        # 両接地なら基本形
        if hand[0] != 0 and hand[-1] != 0:
            return True

        # ゆとりが 1 の時も基本形
        if (hand[0] == 0 and hand[1] != 0 and hand[-1] != 0) or (hand[0] != 0 and hand[-2] != 0 and hand[-1] == 0):
            return True

        # 2番目から始まっていた場合基本形
        if hand[0] == 0 and hand[1] != 0:
            return True

        # それ以外は基本形ではない
        return False


    def getHandGravityPosition(self) -> int:
        """
        牌形の重心を求める

        両端に接地している連続する 0 を無視する。
        両端から見て行った時、大きい数字がある方に重心がある。
        同じ場合はさらに一つ内側で比較する。最後まで一緒なら左右対称形。

        例:
            [0, 2, 4, 0, 0] -> 後方重心
            [0, 2, 2, 3, 2] -> 後方重心
            [0, 2, 2, 1, 2] -> 前方重心
            [0, 2, 1, 1, 2, 0, 0] -> 左右対称形

        Args:
            hand (list[int]): 牌形

        Returns:
            int: 前方重心 1 / 左右対称 0 / 後方重心 -1

        """
        handLength: int = self.length()
        hand = self.hand.copy()

        first: int = 0
        last: int = handLength - 1

        # 前から見たときに初めて 0 でない場所を見つける
        while first < handLength:
            if hand[first] != 0:
                break
            first += 1

        # 後ろから見たときに初めて 0 でない場所を見つける
        while 0 <= last:
            if hand[last] != 0:
                break
            last -= 1

        # 両端から重心を見ていく
        while first < last:
            if hand[first] > hand[last]:
                # 前方重心
                return 1
            if hand[first] < hand[last]:
                # 後方重心
                return -1
            first += 1
            last -= 1

        # 左右対称形
        return 0
