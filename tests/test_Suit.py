import unittest
import src.Suit as Suit

class TestSuit(unittest.TestCase):
    def test_init(self):
        # 長さ8の手牌
        with self.assertRaises(ValueError):
            Suit.Suit([1, 1, 1, 1, 1, 1, 1, 1])

        # 長さ10の手牌
        with self.assertRaises(ValueError):
            Suit.Suit([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

        # マイナスが入っている手牌
        with self.assertRaises(ValueError):
            Suit.Suit([1, 1, 1, 1, 1, 1, 1, 1, -1])

        # 4を超えているものが入っている手牌
        with self.assertRaises(ValueError):
            Suit.Suit([1, 1, 1, 1, 1, 1, 1, 1, 5])

        # 正常系
        suit = Suit.Suit([1, 2, 3, 4, 0, 0, 2, 1, 1])
        self.assertEqual(suit.suit, [1, 2, 3, 4, 0, 0, 2, 1, 1])
