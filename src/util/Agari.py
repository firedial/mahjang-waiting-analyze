from src.util.Suit import Suit
from src.util.WaitingStructure import WaitingStructure
from src.util.WaitingType import WaitingType
import src.util.Remove as Remove


def isAgari(suit: Suit) -> bool:
    """
    渡された数牌が和了形であるかどうかを判定する

    牌の枚数によって判定条件が変わる
        3n + 2 枚のとき: 1 雀頭 n 面子のときに限り和了形
        3n + 1 枚のとき: 和了形にならない
        3n 枚のとき: n 面子のときに限り和了形

    Args:
        suit (Suit): 数牌

    Returns:
        bool: 和了形であれば True / そうでないとき False

    """
    # 手牌の牌の合計枚数
    suitTileCount: int = suit.sum()

    # 手牌の合計枚数が0なら和了形
    if suitTileCount == 0:
        return True

    # 枚数が 3n + 1 場合は和了形にならない
    if suitTileCount % 3 == 1:
        return False

    # 枚数が 3n + 2 場合は頭を除去する
    if suitTileCount % 3 == 2:
        for h in Remove.getRemovedAtamaPatterns(suit):
            if isAgari(h):
                return True
        else:
            return False

    # 3n 枚の時のは面子の除去
    for h in Remove.getRemovedMentsuPatterns(suit):
        if isAgari(h):
            return True
    else:
        return False


def getWaitingStructure(suit: Suit) -> WaitingStructure:
    waitingStructures = []
    for index in range(suit.length()):
        tankiJudgeSuit = suit.getTankiJudgeSuit(index)
        shamponJudgeSuit = suit.getShamponJudgeSuit(index)
        kanchanJudgeSuit = suit.getKanchanJudgeSuit(index)
        ryanmenLeftJudgeSuit = suit.getRyanmenLeftJudgeSuit(index)
        ryanmenRightJudgeSuit = suit.getRyanmenRightJudgeSuit(index)

        waitingStructures.append(
            WaitingType(
                isTanki = False if tankiJudgeSuit is None else isAgari(tankiJudgeSuit),
                isShampon = False if shamponJudgeSuit is None else isAgari(shamponJudgeSuit),
                isKanchan = False if kanchanJudgeSuit is None else isAgari(kanchanJudgeSuit),
                isRyanmenLeft = False if ryanmenLeftJudgeSuit is None else isAgari(ryanmenLeftJudgeSuit),
                isRyanmenRight = False if ryanmenRightJudgeSuit is None else isAgari(ryanmenRightJudgeSuit),
            )
        )

    return WaitingStructure(tuple(waitingStructures))
