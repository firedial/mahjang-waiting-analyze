import unittest
import src.Remove as Remove
from src.Suit import Suit
from src.Block import Block

class TestRemove(unittest.TestCase):
    def test_getRemovedBlockPatterns_1(self):
        suit = Suit((0, 3, 0, 2, 4, 1, 1, 1, 1))
        block = Block((3, 1))
        removedSuits = Remove.getRemovedBlockPatterns(suit, block)

        self.assertEqual(len(removedSuits), 1)
        self.assertEqual(removedSuits[0].suit, (0, 3, 0, 2, 1, 0, 1, 1, 1))

    def test_getRemovedBlockPatterns_2(self):
        suit = Suit((0, 3, 0, 2, 4, 1, 1, 1, 1))
        block = Block((2, ))
        removedSuits = Remove.getRemovedBlockPatterns(suit, block)

        self.assertEqual(len(removedSuits), 3)
        self.assertEqual(removedSuits[0].suit, (0, 1, 0, 2, 4, 1, 1, 1, 1))
        self.assertEqual(removedSuits[1].suit, (0, 3, 0, 0, 4, 1, 1, 1, 1))
        self.assertEqual(removedSuits[2].suit, (0, 3, 0, 2, 2, 1, 1, 1, 1))

    def test_getRemovedMultiBlockPatterns(self):
        suit = Suit((0, 3, 0, 2, 4, 1, 1, 1, 1))
        block = Block((2, ))
        block2 = Block((3, ))
        removedSuits = Remove.getRemovedMultiBlockPatterns(suit, [block, block2])

        self.assertEqual(len(removedSuits), 5)
        self.assertEqual(removedSuits[0].suit, (0, 1, 0, 2, 4, 1, 1, 1, 1))
        self.assertEqual(removedSuits[1].suit, (0, 3, 0, 0, 4, 1, 1, 1, 1))
        self.assertEqual(removedSuits[2].suit, (0, 3, 0, 2, 2, 1, 1, 1, 1))
        self.assertEqual(removedSuits[3].suit, (0, 0, 0, 2, 4, 1, 1, 1, 1))
        self.assertEqual(removedSuits[4].suit, (0, 3, 0, 2, 1, 1, 1, 1, 1))

    def test_getRemovedAtamaPatterns(self):
        suit = Suit((0, 3, 0, 2, 4, 1, 1, 1, 1))
        removedSuits = Remove.getRemovedAtamaPatterns(suit)

        self.assertEqual(len(removedSuits), 3)
        self.assertEqual(removedSuits[0].suit, (0, 1, 0, 2, 4, 1, 1, 1, 1))
        self.assertEqual(removedSuits[1].suit, (0, 3, 0, 0, 4, 1, 1, 1, 1))
        self.assertEqual(removedSuits[2].suit, (0, 3, 0, 2, 2, 1, 1, 1, 1))

    def test_getRemovedAtamaConnectedShuntsuPatterns(self):
        suit = Suit((0, 3, 1, 2, 4, 1, 1, 1, 1))
        removedSuits = Remove.getRemovedAtamaConnectedShuntsuPatterns(suit)

        self.assertEqual(len(removedSuits), 3)
        self.assertEqual(removedSuits[0].suit, (0, 0, 0, 1, 4, 1, 1, 1, 1))
        self.assertEqual(removedSuits[1].suit, (0, 3, 1, 2, 1, 0, 0, 1, 1))
        self.assertEqual(removedSuits[2].suit, (0, 3, 0, 1, 1, 1, 1, 1, 1))

    def test_getRemovedMentsuPatterns(self):
        suit = Suit((0, 3, 0, 2, 4, 1, 1, 1, 1))
        removedSuits = Remove.getRemovedMentsuPatterns(suit)

        self.assertEqual(len(removedSuits), 6)
        self.assertEqual(removedSuits[0].suit, (0, 0, 0, 2, 4, 1, 1, 1, 1))
        self.assertEqual(removedSuits[1].suit, (0, 3, 0, 2, 1, 1, 1, 1, 1))
        self.assertEqual(removedSuits[2].suit, (0, 3, 0, 1, 3, 0, 1, 1, 1))
        self.assertEqual(removedSuits[3].suit, (0, 3, 0, 2, 3, 0, 0, 1, 1))
        self.assertEqual(removedSuits[4].suit, (0, 3, 0, 2, 4, 0, 0, 0, 1))
        self.assertEqual(removedSuits[5].suit, (0, 3, 0, 2, 4, 1, 0, 0, 0))

