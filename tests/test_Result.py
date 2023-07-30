import unittest
import result.waitingPattern
from src.Suit import Suit
from src.Hand import Hand

class TestWaiting(unittest.TestCase):
    def test_waitingPattern(self):
        waitingPatterns = result.waitingPattern.getWaitingPatterns()

        # 全体の数
        self.assertEqual(len(waitingPatterns), 1715)

        # リストに載せる数
        listCount = 0
        atamaConnectedShuntsuCount = 0
        for waitingPattern in waitingPatterns:
            suit = Suit(waitingPattern["suit"])
            hand = Hand(suit)

            if suit.isWaitingBasicForm():
                listCount += 1

            if suit.isBasicForm() and hand.hasAtamaConnectedShuntsuPattern():
                atamaConnectedShuntsuCount += 1

        self.assertEqual(listCount, 319)
        self.assertEqual(atamaConnectedShuntsuCount, 8)



