import unittest
import src.Hand as Hand

class TestHand(unittest.TestCase):
    def test_init(self):
        # 長さ8の手牌
        with self.assertRaises(ValueError):
            Hand.Hand([1, 1, 1, 1, 1, 1, 1, 1])

        # 長さ10の手牌
        with self.assertRaises(ValueError):
            Hand.Hand([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

        # マイナスが入っている手牌
        with self.assertRaises(ValueError):
            Hand.Hand([1, 1, 1, 1, 1, 1, 1, 1, -1])

        # 4を超えているものが入っている手牌
        with self.assertRaises(ValueError):
            Hand.Hand([1, 1, 1, 1, 1, 1, 1, 1, 5])

        # 正常系
        hand = Hand.Hand([1, 2, 3, 4, 0, 0, 2, 1, 1])
        self.assertEqual(hand.hand, [1, 2, 3, 4, 0, 0, 2, 1, 1])
