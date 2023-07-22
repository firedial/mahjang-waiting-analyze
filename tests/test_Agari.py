import unittest
import src.Agari as Agari
import src.Hand as Hand

class TestAgari(unittest.TestCase):
    def test_isAgari(self):
        hand = Hand.Hand([0, 3, 0, 0, 2, 0, 1, 1, 1])
        self.assertTrue(Agari.isAgari(hand))

        hand = Hand.Hand([3, 1, 1, 1, 2, 1, 1, 1, 3])
        self.assertTrue(Agari.isAgari(hand))

        hand = Hand.Hand([2, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertTrue(Agari.isAgari(hand))

        hand = Hand.Hand([2, 0, 3, 3, 0, 3, 3, 0, 0])
        self.assertTrue(Agari.isAgari(hand))
