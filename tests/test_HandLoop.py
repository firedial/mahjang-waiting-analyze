import unittest
import src.Hand as Hand
import src.HandLoop as HandLoop

class TestHandLoop(unittest.TestCase):
    def test_nextHand(self):
        hand = Hand.Hand([0, 0, 0, 0, 0, 0, 0, 0, 1])
        self.assertEqual(HandLoop.nextHand(hand).hand, [0, 0, 0, 0, 0, 0, 0, 1, 0])

        hand = Hand.Hand([3, 0, 0, 0, 0, 0, 0, 0, 1])
        self.assertEqual(HandLoop.nextHand(hand).hand, [0, 0, 0, 0, 0, 0, 0, 4, 0])

        hand = Hand.Hand([0, 0, 0, 0, 0, 0, 0, 3, 1])
        self.assertEqual(HandLoop.nextHand(hand).hand, [0, 0, 0, 0, 0, 0, 1, 2, 1])

        hand = Hand.Hand([0, 0, 0, 0, 0, 0, 1, 2, 1])
        self.assertEqual(HandLoop.nextHand(hand).hand, [0, 0, 0, 0, 0, 1, 0, 2, 1])

        hand = Hand.Hand([4, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(HandLoop.nextHand(hand).hand, [0, 0, 0, 0, 0, 0, 0, 0, 4])

    def test_handLoop(self):
        hand = Hand.Hand([0, 0, 0, 0, 0, 0, 0, 0, 1])
        self.assertEqual(self.countPattern(hand), 9)

        hand = Hand.Hand([0, 0, 0, 0, 0, 0, 0, 0, 2])
        self.assertEqual(self.countPattern(hand), 45)

        hand = Hand.Hand([0, 0, 0, 0, 0, 0, 0, 0, 4])
        self.assertEqual(self.countPattern(hand), 495)

        hand = Hand.Hand([0, 0, 0, 0, 0, 0, 0, 1, 4])
        self.assertEqual(self.countPattern(hand), 1278)

        hand = Hand.Hand([0, 0, 0, 0, 0, 0, 0, 3, 4])
        self.assertEqual(self.countPattern(hand), 6030)

        hand = Hand.Hand([0, 0, 0, 0, 0, 0, 0, 4, 4])
        self.assertEqual(self.countPattern(hand), 11385)

        hand = Hand.Hand([0, 0, 0, 0, 0, 0, 2, 4, 4])
        self.assertEqual(self.countPattern(hand), 32211)

        hand = Hand.Hand([0, 0, 0, 0, 0, 0, 3, 4, 4])
        self.assertEqual(self.countPattern(hand), 48879)

        hand = Hand.Hand([0, 0, 0, 0, 0, 1, 4, 4, 4])
        self.assertEqual(self.countPattern(hand), 93600)


    def countPattern(self, hand: Hand) -> int:
        count: int = 0
        firstHand = hand.hand.copy()
        while True:
            hand = HandLoop.nextHand(hand)
            count += 1
            if (hand.hand == firstHand):
                break
        return count
