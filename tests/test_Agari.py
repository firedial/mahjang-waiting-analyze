import unittest
import src.Agari as Agari
from src.Suit import Suit
from src.Waiting import Waiting

class TestAgari(unittest.TestCase):
    def test_isAgari(self):
        suit = Suit((0, 3, 0, 0, 2, 0, 1, 1, 1))
        self.assertTrue(Agari.isAgari(suit))

        suit = Suit((3, 1, 1, 1, 2, 1, 1, 1, 3))
        self.assertTrue(Agari.isAgari(suit))

        suit = Suit((2, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertTrue(Agari.isAgari(suit))

        suit = Suit((2, 0, 3, 3, 0, 3, 3, 0, 0))
        self.assertTrue(Agari.isAgari(suit))

        suit = Suit((1, 0, 0, 3, 0, 0, 2, 0, 0))
        self.assertFalse(Agari.isAgari(suit))

    def test_getWaiting(self):
        suit = Suit((2, 0, 3, 3, 0, 3, 3, 0, 0))
        waiting = Agari.getWaiting(suit)
        self.assertEqual(waiting.waitingCount, (2, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertTrue(waiting.isSendable)

        suit = Suit((1, 0, 0, 3, 0, 0, 2, 0, 0))
        waiting = Agari.getWaiting(suit)
        self.assertEqual(waiting.waitingCount, (0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertFalse(waiting.isSendable)

        suit = Suit((3, 1, 1, 1, 1, 1, 1, 1, 3))
        waiting = Agari.getWaiting(suit)
        self.assertEqual(waiting.waitingCount, (1, 3, 3, 3, 3, 3, 3, 3, 1))
        self.assertFalse(waiting.isSendable)

        # 4枚使いは聴牌にならない
        suit = Suit((0, 4, 0, 0, 0, 0, 0, 0, 0))
        waiting = Agari.getWaiting(suit)
        self.assertEqual(waiting.waitingCount, (0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertFalse(waiting.isSendable)
