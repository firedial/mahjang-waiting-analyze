import unittest
from src.util.Suit import Suit

class TestSuit(unittest.TestCase):
    def test_init(self):
        # 長さ8の手牌
        with self.assertRaises(ValueError):
            Suit((1, 1, 1, 1, 1, 1, 1, 1))

        # 長さ10の手牌
        with self.assertRaises(ValueError):
            Suit((1, 1, 1, 1, 1, 1, 1, 1, 1, 1))

        # マイナスが入っている手牌
        with self.assertRaises(ValueError):
            Suit((1, 1, 1, 1, 1, 1, 1, 1, -1))

        # 4を超えているものが入っている手牌
        with self.assertRaises(ValueError):
            Suit((1, 1, 1, 1, 1, 1, 1, 1, 5))

        # 正常系
        suit = Suit((1, 2, 3, 4, 0, 0, 2, 1, 1))
        self.assertEqual(suit.suit, (1, 2, 3, 4, 0, 0, 2, 1, 1))

    def test_length(self):
        suit = Suit((1, 2, 3, 4, 0, 0, 2, 1, 1))
        self.assertEqual(suit.length(), 9)

    def test_sum(self):
        suit = Suit((1, 2, 3, 4, 0, 0, 2, 1, 1))
        self.assertEqual(suit.sum(), 14)

        suit = Suit((1, 0, 3, 0, 0, 0, 2, 1, 1))
        self.assertEqual(suit.sum(), 8)

    def test_isFirstTIleZero(self):
        suit = Suit((1, 2, 3, 4, 0, 0, 2, 0, 0))
        self.assertFalse(suit.isFirstTIleZero())

        suit = Suit((0, 2, 3, 4, 0, 0, 2, 0, 0))
        self.assertTrue(suit.isFirstTIleZero())

    def test_getRightAttachSuit(self):
        suit = Suit((0, 2, 3, 4, 0, 0, 2, 3, 0))
        self.assertEqual(suit.getRightAttachSuit(), Suit((0, 0, 2, 3, 4, 0, 0, 2, 3)))

        suit = Suit((0, 2, 3, 4, 0, 0, 0, 0, 0))
        self.assertEqual(suit.getRightAttachSuit(), Suit((0, 0, 0, 0, 0, 0, 2, 3, 4)))

    def test_isBasicForm(self):
        suit = Suit((0, 2, 3, 4, 0, 0, 2, 3, 0))
        self.assertFalse(suit.isBasicForm())

        suit = Suit((0, 4, 3, 4, 0, 0, 2, 3, 0))
        self.assertTrue(suit.isBasicForm())

        suit = Suit((0, 0, 4, 3, 4, 0, 0, 2, 3))
        self.assertFalse(suit.isBasicForm())

        suit = Suit((0, 4, 4, 3, 4, 0, 0, 2, 3))
        self.assertTrue(suit.isBasicForm())

        suit = Suit((4, 4, 3, 4, 0, 0, 2, 3, 0))
        self.assertFalse(suit.isBasicForm())

        suit = Suit((4, 4, 3, 4, 0, 0, 2, 3, 1))
        self.assertTrue(suit.isBasicForm())

        suit = Suit((1, 2, 3, 4, 0, 0, 2, 3, 1))
        self.assertFalse(suit.isBasicForm())
