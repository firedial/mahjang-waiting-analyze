import unittest
from src.Hand import Hand
from src.Suit import Suit

class TestHand(unittest.TestCase):
    def test_init(self):
        hand = Hand(Suit((3, 1, 1, 1, 1, 1, 1, 1, 3)))
        self.assertEqual(hand.waiting.waitingCount, (1, 3, 3, 3, 3, 3, 3, 3, 1))
        self.assertFalse(hand.isAtamaConnectedShuntsu)

        hand = Hand(Suit((3, 1, 1, 0, 0, 0, 0, 0, 0)), True)
        self.assertEqual(hand.waiting.waitingCount, (1, 0, 0, 4, 0, 0, 0, 0, 0))
        self.assertTrue(hand.isAtamaConnectedShuntsu)

    def test_isTempai(self):
        hand = Hand(Suit((3, 1, 1, 0, 0, 0, 0, 0, 0)), True)
        self.assertTrue(hand.isTempai())

    def test_isBasicForm(self):
        hand = Hand(Suit((3, 1, 1, 0, 0, 0, 0, 0, 0)))
        self.assertFalse(hand.isBasicForm())

    def test_isRegularForm(self):
        hand = Hand(Suit((3, 1, 1, 0, 0, 0, 0, 0, 0)))
        self.assertFalse(hand.isRegularForm())

    def test_getWaitingTileCountWithAtama(self):
        hand = Hand(Suit((0, 1, 1, 1, 1, 0, 0, 0, 0)))
        self.assertEqual(hand.getWaitingTileCountWithAtama(), 2)

        hand = Hand(Suit((3, 1, 1, 0, 0, 0, 0, 0, 0)))
        self.assertEqual(hand.getWaitingTileCountWithAtama(), 3)

        hand = Hand(Suit((3, 1, 1, 0, 0, 0, 0, 0, 0)), True)
        self.assertEqual(hand.getWaitingTileCountWithAtama(), 4)

    def test_isIrreducible(self):
        hand = Hand(Suit((0, 1, 1, 1, 1, 0, 0, 0, 0)))
        self.assertTrue(hand.isIrreducible())

        hand = Hand(Suit((0, 1, 1, 0, 0, 0, 0, 0, 0)))
        self.assertTrue(hand.isIrreducible())

        hand = Hand(Suit((1, 1, 1, 1, 1, 0, 0, 0, 0)))
        self.assertFalse(hand.isIrreducible())

    def test___lt__(self):
        hand1 = Hand(Suit((1, 1, 1, 1, 1, 0, 0, 0, 0)))
        hand2 = Hand(Suit((0, 0, 0, 1, 1, 0, 0, 0, 0)))
        self.assertFalse(hand2 < hand1)

        hand1 = Hand(Suit((1, 1, 1, 1, 1, 0, 0, 0, 0)))
        hand2 = Hand(Suit((1, 1, 0, 0, 0, 0, 0, 0, 0)))
        self.assertTrue(hand2 < hand1)
