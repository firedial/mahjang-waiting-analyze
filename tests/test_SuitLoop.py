import unittest
import src.Suit as Suit
import src.SuitLoop as SuitLoop

class TestSuitLoop(unittest.TestCase):
    def test_nextSuit(self):
        suit = Suit.Suit([0, 0, 0, 0, 0, 0, 0, 0, 1])
        self.assertEqual(SuitLoop.nextSuit(suit).suit, [0, 0, 0, 0, 0, 0, 0, 1, 0])

        suit = Suit.Suit([3, 0, 0, 0, 0, 0, 0, 0, 1])
        self.assertEqual(SuitLoop.nextSuit(suit).suit, [0, 0, 0, 0, 0, 0, 0, 4, 0])

        suit = Suit.Suit([0, 0, 0, 0, 0, 0, 0, 3, 1])
        self.assertEqual(SuitLoop.nextSuit(suit).suit, [0, 0, 0, 0, 0, 0, 1, 2, 1])

        suit = Suit.Suit([0, 0, 0, 0, 0, 0, 1, 2, 1])
        self.assertEqual(SuitLoop.nextSuit(suit).suit, [0, 0, 0, 0, 0, 1, 0, 2, 1])

        suit = Suit.Suit([4, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(SuitLoop.nextSuit(suit).suit, [0, 0, 0, 0, 0, 0, 0, 0, 4])


    def test_suitLoop(self):
        suit = Suit.Suit([0, 0, 0, 0, 0, 0, 0, 0, 1])
        self.assertEqual(self.countPattern(suit), 9)

        suit = Suit.Suit([0, 0, 0, 0, 0, 0, 0, 0, 2])
        self.assertEqual(self.countPattern(suit), 45)

        suit = Suit.Suit([0, 0, 0, 0, 0, 0, 0, 0, 4])
        self.assertEqual(self.countPattern(suit), 495)

        suit = Suit.Suit([0, 0, 0, 0, 0, 0, 0, 1, 4])
        self.assertEqual(self.countPattern(suit), 1278)

        suit = Suit.Suit([0, 0, 0, 0, 0, 0, 0, 3, 4])
        self.assertEqual(self.countPattern(suit), 6030)

        suit = Suit.Suit([0, 0, 0, 0, 0, 0, 0, 4, 4])
        self.assertEqual(self.countPattern(suit), 11385)

        suit = Suit.Suit([0, 0, 0, 0, 0, 0, 2, 4, 4])
        self.assertEqual(self.countPattern(suit), 32211)

        suit = Suit.Suit([0, 0, 0, 0, 0, 0, 3, 4, 4])
        self.assertEqual(self.countPattern(suit), 48879)

        suit = Suit.Suit([0, 0, 0, 0, 0, 1, 4, 4, 4])
        self.assertEqual(self.countPattern(suit), 93600)


    def countPattern(self, suit: Suit) -> int:
        count: int = 0
        firstSuit = suit.suit.copy()
        while True:
            suit = SuitLoop.nextSuit(suit)
            count += 1
            if (suit.suit == firstSuit):
                break
        return count
