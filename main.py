from src.Suit import Suit
from src.Hand import Hand
from src.WaitingPatternUtil import WaitingPatternUtil
import src.Agari

waitingPatternUtil = WaitingPatternUtil()
hand = Hand(Suit((0, 0, 1, 1, 3, 0, 0, 0, 0)), True)

num = waitingPatternUtil.getWaitingPatternNumber(hand)
print(num)

suit = Suit((0, 0, 1, 1, 3, 0, 0, 0, 0))
print(suit.getRyanmenRightJudgeSuit(4))

s = src.Agari.getWaitingStructure(suit)
print(s)

print(hand.waitingStructure)