import unittest
from src.Suit import Suit

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

    def test_isRegularForm(self):
        suit = Suit((1, 2, 3, 4, 0, 0, 0, 0, 1))
        self.assertFalse(suit.isRegularForm())

        suit = Suit((1, 0, 3, 4, 0, 0, 2, 0, 0))
        self.assertTrue(suit.isRegularForm())

        suit = Suit((1, 2, 3, 4, 0, 0, 2, 0, 0))
        self.assertFalse(suit.isRegularForm())

    def test_isFirstTIleZero(self):
        suit = Suit((1, 2, 3, 4, 0, 0, 2, 0, 0))
        self.assertFalse(suit.isFirstTIleZero())

        suit = Suit((0, 2, 3, 4, 0, 0, 2, 0, 0))
        self.assertTrue(suit.isFirstTIleZero())

    def test_getRemainTileCount(self):
        suit = Suit((0, 2, 3, 4, 0, 0, 2, 0, 0))
        self.assertEqual(suit.getRemainTileCount(0), 4)
        self.assertEqual(suit.getRemainTileCount(1), 2)
        self.assertEqual(suit.getRemainTileCount(3), 0)

    def test_addTile(self):
        suit = Suit((0, 2, 3, 4, 0, 0, 2, 0, 0))

        addSuit = suit.addTile(0)
        self.assertEqual(addSuit.suit[0], 1)

        addSuit = suit.addTile(3)
        self.assertIsNone(addSuit)

    def test_getOneLeftSuit(self):
        suit = Suit((0, 2, 3, 4, 0, 0, 2, 0, 0))

        leftSuit = suit.getOneLeftSuit()
        self.assertEqual(leftSuit, Suit((2, 3, 4, 0, 0, 2, 0, 0, 0)))

        lettSuit = leftSuit.getOneLeftSuit()
        self.assertEqual(lettSuit, Suit((3, 4, 0, 0, 2, 0, 0, 0, 0)))

    def test_getOneRightSuit(self):
        suit = Suit((0, 2, 3, 4, 0, 0, 2, 3, 0))

        rightSuit = suit.getOneRightSuit()
        self.assertEqual(rightSuit, Suit((0, 0, 2, 3, 4, 0, 0, 2, 3)))

        rightSuit = rightSuit.getOneRightSuit()
        self.assertEqual(rightSuit, Suit((0, 0, 0, 2, 3, 4, 0, 0, 2)))

    def test_getRightAttachSuit(self):
        suit = Suit((0, 2, 3, 4, 0, 0, 2, 3, 0))
        self.assertEqual(suit.getRightAttachSuit(), Suit((0, 0, 2, 3, 4, 0, 0, 2, 3)))

        suit = Suit((0, 2, 3, 4, 0, 0, 0, 0, 0))
        self.assertEqual(suit.getRightAttachSuit(), Suit((0, 0, 0, 0, 0, 0, 2, 3, 4)))

    def test_getReverseSuit(self):
        suit = Suit((0, 2, 3, 4, 0, 0, 2, 3, 0))
        self.assertEqual(suit.getReverseSuit(), Suit((0, 3, 2, 0, 0, 4, 3, 2, 0)))

    def test_getRange(self):
        suit = Suit((0, 2, 3, 4, 0, 0, 2, 3, 0))
        self.assertEqual(suit.getRange(), 7)

        suit = Suit((1, 2, 3, 4, 0, 0, 2, 3, 0))
        self.assertEqual(suit.getRange(), 8)

        suit = Suit((1, 2, 3, 4, 0, 0, 2, 3, 2))
        self.assertEqual(suit.getRange(), 9)

        suit = Suit((0, 0, 0, 0, 0, 0, 2, 0, 0))
        self.assertEqual(suit.getRange(), 1)

    def test_getPosition(self):
        suit = Suit((0, 2, 3, 4, 0, 0, 2, 3, 0))
        self.assertEqual(suit.getPosition(), 1)

        suit = Suit((0, 0, 0, 4, 0, 0, 2, 3, 0))
        self.assertEqual(suit.getPosition(), 3)

        suit = Suit((1, 0, 0, 4, 0, 0, 2, 3, 0))
        self.assertEqual(suit.getPosition(), 0)

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
        self.assertTrue(suit.isBasicForm())

        suit = Suit((4, 4, 3, 4, 0, 0, 2, 3, 1))
        self.assertTrue(suit.isBasicForm())

        suit = Suit((1, 2, 3, 4, 0, 0, 2, 3, 1))
        self.assertFalse(suit.isBasicForm())

    def test_getSuitGravityPosition(self):
        suit = Suit((1, 2, 3, 4, 0, 0, 2, 3, 1))
        self.assertEqual(suit.getSuitGravityPosition(), -1)

        suit = Suit((1, 4, 3, 4, 0, 0, 2, 3, 1))
        self.assertEqual(suit.getSuitGravityPosition(), 1)

        suit = Suit((1, 3, 2, 0, 0, 0, 2, 3, 1))
        self.assertEqual(suit.getSuitGravityPosition(), 0)
